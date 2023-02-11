
namespace UpwardFarms.Scantron.ViewModels
{
    using System;
    using System.Collections.Generic;
    using System.Collections.ObjectModel;
    using System.Linq;
    using System.Text;
    using System.Threading.Tasks;
    using System.Windows.Input;

    using TechnologySolutions.Rfid.AsciiProtocol;
    using TechnologySolutions.Rfid.AsciiProtocol.Extensions;
    using TechnologySolutions.Rfid.AsciiProtocol.Transports;

    using Xamarin.Essentials;
    using Models;
    using Services;
    using System.Web;

    public class MainViewModel
        : ViewModelBase, ILifecycle
    {
        public enum OpMode
        {
            ScanInfo,
            Inventory,
            JobSelectJob,
            JobScan,
            JobSubmit,
            JobComplete,
            ManualInfo,
            Settings
        };

        private const int ADVANCED_SETTING_COUNTER_THRESHOLD = 5;

        // UI Control
        private OpMode opMode = OpMode.ScanInfo;
        private bool enablePopup;
        private bool firstShow = true;
        private bool isRefreshing = false;
        private bool showSpinner = false;
        private bool isReaderConfiguring;
        private bool showAdvancedOptions = false;
        private int  showAdvancedCounter = 0;
        private string bluetoothAddressText;

        private string curJob = null;
        private string curProgressString = "Scan Raft(s)";
        private string curScanProgressColor = "#c9df9e";
        private int curScanCount = 0;
        private int curScanLimit = 0;

        // UI Command Interfaces (Configured As Callbacks)
        public ICommand TapConfigLabel { get; private set; }
        public ICommand TapInfoModeLabel { get; private set; }
        public ICommand TapManualModeLabel { get; private set; }
        public ICommand TapJobSelectModeLabel { get; private set; }
        public ICommand TapSettingsModeLabel { get; private set; }
        public ICommand TapInventoryModeLabel { get; private set; }
        public ICommand TapInventoryLabel { get; private set; }
        public ICommand TapMainIcon { get; private set; }
        public ICommand ScannerConfigUpdateCommand { get; private set; }
        public ICommand ConfigCommand { get; private set; }
        public ICommand AddNewCommand { get; private set; }
        public ICommand RefreshScannersCommand { get; private set; }
        public ICommand RefreshJobsCommand { get; private set; }
        public ICommand RefreshCompaniesCommand { get; private set; }
        public ICommand PairAndConnectCommand { get; private set; }
        public ICommand UnpairAndDisconnectCommand { get; private set; }

        // Application Configuration Options 
        private int hostSelect;
        private AppConfiguration appConfiguration;
        private IInventoryConfigurator scannerConfigurator;
        public InventoryConfiguration scannerConfiguration { get; private set; }

        // Interfaces for Dealing with Scanners
        private readonly IAsciiTransportsManager transportsManager;
        private IAsciiTransportEnumerator addNewEnumerator;
        public ObservableCollection<ScannerViewModel> Scanners { get; private set; } = new ObservableCollection<ScannerViewModel>();

        // Raft Inventory Control
        public RaftInventory raftInventory;
        public ObservableCollection<IdentifiedItem> Rafts { get; private set; }

        // Scan Job Inventory Control
        public ScanJobInventory scanJobInventory;
        public ObservableCollection<FarmRescanJobInfo> Jobs { get; private set; }

        // Company Inventory Control
        public CompanyInventory companyInventory;
        public ObservableCollection<FarmCompanyInfo> Companies { get; private set; }
        private FarmCompanyInfo selectedCompany;

        // Init
        // ====

        public MainViewModel(IAsciiTransportsManager transportsManager,
                             AppConfiguration appConfiguration,
                             RaftInventory raftInventory,
                             ScanJobInventory scanJobInventory,
                             CompanyInventory companyInventory,
                             IInventoryConfigurator scannerConfigurator,
                             InventoryConfiguration scannerConfiguration)
        {
            // This is our application Configuration
            this.appConfiguration = appConfiguration;

            // This is our transport manager (for searching for Scanners, etc)
            this.transportsManager = transportsManager ?? throw new ArgumentNullException("transportsManager");

            // This is our raft Inventory Storage (and a shorthand for the list to used by the GUI)
            this.raftInventory = raftInventory;
            Rafts = this.raftInventory.Identifiers;
            this.raftInventory.OnCountUpdated = this.OnCountUpdated;

            // This is our job Inventory Storage (and a shorthand for the list to used by the GUI)
            this.scanJobInventory = scanJobInventory;
            Jobs = this.scanJobInventory.Jobs;

            // This is our company Inventory Storage (and a shorthand for the list to used by the GUI)
            this.companyInventory = companyInventory;
            Companies = this.companyInventory.Companies;

            // This is our scanner interface (The configurator control object and our actual configuration)
            this.scannerConfigurator = scannerConfigurator;
            this.scannerConfiguration = scannerConfiguration;

            // Set up a callback for ScannerFound with e.Transport but on the UI thread
            IProgress<IAsciiTransport>  transportsManagerDispatcher = new Progress<IAsciiTransport>(ScannerFound);            
            this.transportsManager.TransportChanged += (sender, e) => transportsManagerDispatcher.Report(e.Transport);
            
            // The transports manager has a number of enumerators, each one enumerating a particular transport type.
            // Typically we expect only one of the enumerators to support AddNew (where a UI can be show to add a new reader to the list)
            // In any case we'll only support showing the UI for the first enumerator that does
            // Pick the first enumerator that supports AddNew (CanShowAddNew == true) and if we have one wire it up to the AddNewCommand (plus top right on UI, assuming default view)
            addNewEnumerator = this.transportsManager.Enumerators.Where(enumerator => enumerator.CanShowAddNew).FirstOrDefault();
            AddNewCommand = new RelayCommand(() => { addNewEnumerator?.ShowAddNew(); }, () => { return addNewEnumerator != null; });

            // Refresh Scanners command (Force all the scanner enumerators to revisit and return the list of available transports)
            RefreshScannersCommand = new RelayCommand(async () => await ExecuteRefreshScannersAsync());
            RefreshJobsCommand = new RelayCommand(async () => await ExecuteRefreshJobsAsync());
            RefreshCompaniesCommand = new RelayCommand(async () => await ExecuteRefreshCompaniesAsync());

            // Bluetooth Security commands
            PairAndConnectCommand = new RelayCommand(async () => await ExecutePairAndConnectAsync(), CanExecutePairAndConnect);
            UnpairAndDisconnectCommand = new RelayCommand(async () => await ExecuteUnpairAndDisconnectAsync(), CanExecuteUnpairAndDisconnect);
            BluetoothAddressText = "88:6B:0F:31:90:83"; // 2128 - 000215

            // Connect Callbacks for working with raft inventory
            ScannerConfigUpdateCommand = new RelayCommand(UpdateScannerConfig, CanUpdateScannerConfig);
            this.scannerConfiguration.PropertyChanged += (sender, e) =>
            {
                object propertyValue = sender.GetType().GetProperty(e.PropertyName).GetValue(sender);
                ScannerConfigUpdateCommand.RefreshCanExecute();
            };

            // Connect Label Tapping Callbacks
            TapMainIcon = new RelayCommand(OnPopupClicked, CanTapConfigLabel);
            TapConfigLabel = new RelayCommand(OnTapConfigLabel, CanTapConfigLabel);
            TapInfoModeLabel = new RelayCommand(OnInfoModeTapped, CanTapConfigLabel);
            TapManualModeLabel = new RelayCommand(OnManualModeTapped, CanTapConfigLabel);
            TapJobSelectModeLabel = new RelayCommand(OnJobSelectModeTapped, CanTapConfigLabel);
            TapSettingsModeLabel = new RelayCommand(OnSettingsModeTapped, CanTapConfigLabel);
            TapInventoryModeLabel = new RelayCommand(OnInventoryModeTapped, CanTapConfigLabel);

            // Track Version Information
            VersionTracking.Track();

            // Configure Initial Settings
            IsReaderConfiguring = false;
            enablePopup = false;
            hostSelect = 1;
        }

        // Show / Hide Application
        // =======================

        public async void Shown()
        {
            // ensure all the enumerators are started
            foreach(var enumerator in transportsManager.Enumerators )
            {
                if (enumerator.State == EnumerationState.Created)
                {
                    enumerator.Start();
                }
            }

            raftInventory.IsEnabled = true;
            if (firstShow)
            {
                // Configure the Scanner
                scannerConfiguration.UpdateAll();
                scannerConfiguration.OutputPower = (int)(appConfiguration.PowerLevelInfo);
                ScannerConfigUpdateCommand.RefreshCanExecute();

                // Set the default Company
                selectedCompany = null;
                await companyInventory.Refresh();
                var readableName = HttpUtility.UrlDecode(appConfiguration.CompanyName);
                foreach (var company in Companies)
                {
                    if (company.Name == readableName)
                    {
                        SelectedCompany = company;
                        appConfiguration.CompanyId = company.Id;
                        break;
                    }
                }

                firstShow = false;
            }
        }

        public void Hidden()
        {
            raftInventory.IsEnabled = false;
        }

        // Raft Inventory: Clearing
        // ========================

        // Look for Rafts
        public void ClearRafts()
        {
            try
            {
                raftInventory.Clear();
                CurScanCount = 0;
            }
            catch (Exception ex)
            {
                ReportError(ex);
            }
        }

        // Handle Removing a Single Item
        public void DeleteRaft(IdentifiedItem raft)
        {
            if ((raft != null) && (Rafts.IndexOf(raft) >= 0))
            {
                Rafts.Remove(raft);
                if (CurScanCount > 0)
                {
                    CurScanCount--;
                }
            }
        }

        // Scanner: Search
        // ===============

        // Look for Scanners (This includes preconfigured scanners)
        private async Task ExecuteRefreshScannersAsync()
        {
            IsRefreshing = true;
            try
            {
                foreach (var enumerator in transportsManager.Enumerators)
                {
                    await enumerator.ListAsciiTransportsAsync();
                }
            }
            catch (Exception ex)
            {
                ReportError(ex);
            }
            IsRefreshing = false;
        }

        // Handle notifications for scanner refreshes
        public bool IsRefreshing
        {
            get { return isRefreshing; }
            set
            {
                isRefreshing = value;
                RaisePropertyChanged(nameof(IsRefreshing));
            }
        }

        // Handle new scanners being detected
        private void ScannerFound(IAsciiTransport scanner)
        {
            if (scanner.State == ConnectionState.Available)
            {
                // Add a Transport (Scanner) to the list if (1) It's not already there and (2) It's Display Name ends with "-1166"
                var viewModel = Scanners.Where(vm => vm.Id == scanner.Id).FirstOrDefault();
                if ((viewModel == null) && (scanner.DisplayName.EndsWith("-1166")))
                {
                    viewModel = new ScannerViewModel(transportsManager, scanner);
                    Scanners.Add(viewModel);

                    // Attempt to Automatically Connect (This is launched but we don't wait for completion)
                    BluetoothAddressText = viewModel.Id;
                    _ = ExecutePairAndConnectAsync();
                }
            }
        }

        // Bindable Interface: Control Bluetooth Address
        public string BluetoothAddressText
        {
            get => bluetoothAddressText;
            set => Set(ref bluetoothAddressText, value);
        }

        // Scanner: Connect
        // ================

        // Allow ourselves to pair with a Scanner
        private bool CanExecutePairAndConnect()
        {
            return transportsManager.BluetoothSecurity.CanPair;
        }

        // Pair and Connect to a Scanner
        private async Task ExecutePairAndConnectAsync()
        {
            try
            {
                BluetoothAddress address = BluetoothAddress.Parse(BluetoothAddressText);

                var result = await transportsManager.BluetoothSecurity.PairAsync(address);
                if (!result )
                {
                    throw new ApplicationException(string.Format("Failed to pair to {0}", BluetoothAddressText));
                }

                var transports = await transportsManager.Enumerators
                    .Where(t => t.Physical == PhysicalTransport.Bluetooth).FirstOrDefault()
                    ?.ListAsciiTransportsAsync() ?? new List<IAsciiTransport>();

                var transport = transports.Where(t => t.DisplayInfoLine.Contains(address.ToString())).FirstOrDefault();

                if (transport != null)
                {
                    await transport.ConnectAsync();
                }

            }
            catch(FormatException fe)
            {
                ReportError(fe, "ConnectionsView");
            }
            catch (Exception ex)
            {
                ReportError(ex, "ConnectionsView");
            }
        }

        // Scanner: Disconnect
        // ===================

        // Allow ourselves to disconnect from a scanner
        private bool CanExecuteUnpairAndDisconnect()
        {
            return transportsManager.BluetoothSecurity.CanUnpair;
        }

        // Disconnect and Unpair from a Scanner
        private async Task ExecuteUnpairAndDisconnectAsync()
        {
            try
            {
                BluetoothAddress address = BluetoothAddress.Parse(BluetoothAddressText);

                var result = await transportsManager.BluetoothSecurity.UnpairAsync(address);
                if (!result)
                {
                    throw new ApplicationException(string.Format("Failed to unpair to {0}", BluetoothAddressText));
                }                
            }
            catch (FormatException fe)
            {
                ReportError(fe, "ConnectionsView");
            }
            catch (Exception ex)
            {
                ReportError(ex, "ConnectionsView");
            }
        }

        // Scanner: Configuration
        // ======================

        // We Allow Configuration When Not Already Configuring and We Have Local Changes
        private bool CanUpdateScannerConfig()
        {
            return !IsReaderConfiguring && scannerConfiguration.IsChanged;
        }

        // Perform the Configuration
        private async void UpdateScannerConfig()
        {
            IsReaderConfiguring = true;

            await scannerConfigurator.ConfigureAsync();
            scannerConfiguration.UpdateAll();

            IsReaderConfiguring = false;
        }

        // Bindable Interface: Is the Scanner currently being configured?
        private bool IsReaderConfiguring
        {
            get
            {
                return isReaderConfiguring;
            }

            set
            {
                Set(ref isReaderConfiguring, value);
                ScannerConfigUpdateCommand.RefreshCanExecute();
            }
        }

        // Title Bar
        // =========

        // Handle popup menus
        public void OnPopupClicked()
        {
            EnablePopup = !EnablePopup;
        }


        // Assemble the Title from the Actual Version!
        public string Version
        {
            get
            {
                return "Upward Farms Scantron v" + VersionTracking.CurrentVersion + "." + VersionTracking.CurrentBuild;
            }
        }

        // Popup Control & Sections
        // ========================

        // Bindable Interface: Is Popup Panel Being Shown? 
        public bool EnablePopup
        {
            get
            {
                return enablePopup;
            }

            set
            {
                Set(ref enablePopup, value);
            }
        }

        // Bindable Interface: Current Op Modes Shown 
        public OpMode CurOpMode
        {
            get
            {
                return opMode;
            }

            set
            {
                Set(ref opMode, value);

                // Notify all panels to refresh
                RaisePropertyChanged("ShowSettingsPanel");
                RaisePropertyChanged("ShowJobHeader");
                RaisePropertyChanged("ShowJobSelectPanel");
                RaisePropertyChanged("ShowManualPanel");
                RaisePropertyChanged("ShowScanPanel");
                RaisePropertyChanged("ShowScanProgressPanel");
                RaisePropertyChanged("ShowJobAcceptPanel");
                RaisePropertyChanged("ShowScanComplete");
                RaisePropertyChanged("ShowInventory");
                RaisePropertyChanged("CurScanProgress");
            }
        }

        // Bindable Interface: Current Job Being Worked On
        public string CurJob
        {
            get
            {
                return curJob;
            }

            set
            {
                Set(ref curJob, value);
            }
        }

        // Bindable Interface: Current Job Scan Count
        public int CurScanCount
        {
            get
            {
                return curScanCount;
            }

            set
            {
                Set(ref curScanCount, value);

                if ((curScanLimit <= 0) || (curScanCount < curScanLimit))
                    CurScanProgressColor = "#c9df9e";
                else if (curScanCount == curScanLimit)
                    CurScanProgressColor = "#2ca858";
                else
                    CurScanProgressColor = "#f28f40";

                RaisePropertyChanged("ShowJobAcceptPanel");
                RaisePropertyChanged("CurScanProgress");
            }
        }

        public void OnCountUpdated(int newCount)
        {
            CurScanCount = newCount;
        }

        // Bindable Interface: Current Job Scan Limit
        public int CurScanLimit
        {
            get
            {
                return curScanLimit;
            }

            set
            {
                Set(ref curScanLimit, value);

                if ((curScanLimit <= 0) || (curScanCount < curScanLimit))
                    CurScanProgressColor = "#c9df9e";
                else if (curScanCount == curScanLimit)
                    CurScanProgressColor = "#2ca858";
                else
                    CurScanProgressColor = "#f28f40";
            }
        }

        public string CurScanProgress
        {
            get
            {
                if (curScanLimit <= 0)
                {
                    if (curScanCount < 1)
                        return "Scan Raft(s)";
                    else
                        return "Scanned " + curScanCount.ToString() + " Rafts";
                }
                else
                {
                    if (curScanLimit == 1)
                        return curProgressString + "Scanned " + curScanCount.ToString() + " of 1 Raft for Job";
                    else
                        return curProgressString + "Scanned " + curScanCount.ToString() + " of " + curScanLimit.ToString() + " Rafts for Job";
                }
            }

            set
            {
                if (value.Length == 0)
                    Set(ref curProgressString, value);
                else
                    Set(ref curProgressString, value + "\n");
            }
        }

        public string CurScanProgressColor
        {
            get
            {
                return curScanProgressColor;
            }

            set
            {
                Set(ref curScanProgressColor, value);
            }
        }

        // Getters for Controlling On-Screen Controls Based on Mode (Add each to the list above)
        public bool ShowSettingsPanel
        {
            get
            {
                return CurOpMode == OpMode.Settings;
            }
        }

        public bool ShowInventory
        {
            get
            {
                return CurOpMode == OpMode.Inventory;
            }
        }

        public bool ShowJobHeader
        {
            get
            {
                return (CurOpMode == OpMode.JobScan) || (CurOpMode == OpMode.JobSubmit) || (CurOpMode == OpMode.JobComplete);
            }
        }

        public bool ShowJobSelectPanel
        {
            get
            {
                return CurOpMode == OpMode.JobSelectJob;
            }
        }

        public bool ShowManualPanel
        {
            get
            {
                return CurOpMode == OpMode.ManualInfo;
            }
        }

        public bool ShowScanPanel
        {
            get
            {
                return (CurOpMode == OpMode.ScanInfo) || (CurOpMode == OpMode.ManualInfo) || (CurOpMode == OpMode.JobScan) || (CurOpMode == OpMode.JobSubmit);
            }
        }

        public bool ShowScanProgressPanel
        {
            get
            {
                return (CurOpMode == OpMode.ScanInfo) || (CurOpMode == OpMode.Inventory) || (CurOpMode == OpMode.ManualInfo) || (CurOpMode == OpMode.JobScan) || (CurOpMode == OpMode.JobSubmit);
            }
        }

        public bool ShowJobAcceptPanel
        {
            get
            {
                return (CurOpMode == OpMode.JobScan) && (CurScanCount == CurScanLimit);
            }
        }

        public bool ShowScanComplete
        {
            get
            {
                return (CurOpMode == OpMode.JobComplete);
            }
        }

        public void OnSelectMode(OpMode newMode)
        {
            CurOpMode = newMode;
            CurScanLimit = 0;
            CurScanProgress = "";
            EnablePopup = false;

            ClearRafts();

            // Set Power Level
            if ((newMode == OpMode.ScanInfo) || (newMode == OpMode.ManualInfo))
            {
                scannerConfiguration.OutputPower = (int)(appConfiguration.PowerLevelInfo);
            }
            else if (newMode == OpMode.Inventory)
            {
                scannerConfiguration.OutputPower = (int)(appConfiguration.PowerLevelInventory);
            }
            else 
            {
                scannerConfiguration.OutputPower = (int)(appConfiguration.PowerLevelJob);
            }
            UpdateScannerConfig();
        }

        private async void OnInfoModeTapped()
        {
            OnSelectMode(OpMode.ScanInfo);
        }

        private async void OnManualModeTapped()
        {
            OnSelectMode(OpMode.ManualInfo);
        }

        private async void OnJobSelectModeTapped()
        {
            OnSelectMode(OpMode.JobSelectJob);
            ExecuteRefreshJobsAsync();
        }

        private async void OnSettingsModeTapped()
        {
            OnSelectMode(OpMode.Settings);
        }

        private async void OnInventoryModeTapped()
        {
            OnSelectMode(OpMode.Inventory);
        }

        // We always allow the label to be tapped.
        private bool CanTapConfigLabel()
        {
            return true;
        }

        //
        public async Task<string> PostJobValidation()
        {
            ShowSpinner = true;
            string err = await raftInventory.PostRescanJob(CurJob, CurScanLimit);
            ShowSpinner = false;
            return err;
        }

        // Activity Spinner Popup
        public bool ShowSpinner
        {
            get
            {
                return showSpinner;
            }

            set
            {
                Set(ref showSpinner, value);
            }
        }

        // Configuration Popup
        // ===================

        // Enable Advanced Settings
        public bool EnabledAdvancedSettings
        {
            get
            {
                return showAdvancedOptions;
            }

            set
            {
                Set(ref showAdvancedOptions, value);
            }
        }

        public void OnTapConfigLabel()
        {
            if (showAdvancedOptions)
            {
                showAdvancedCounter = 0;
                EnabledAdvancedSettings = false;
            }
            else
            {
                showAdvancedCounter++;
                if (showAdvancedCounter >= ADVANCED_SETTING_COUNTER_THRESHOLD)
                {
                    EnabledAdvancedSettings = true;
                }
            }
        }

        // Bindable Interface: Should the Application Show a line for Manual ID Entry?
        public bool EnableManualEntry
        {
            get
            {
                return appConfiguration.EnableManualId;
            }

            set
            {
                appConfiguration.EnableManualId = value;
                RaisePropertyChanged("EnableManualEntry");
            }
        }

        // Bindable Interface: Should the Application Replace Scans with Built-in Test Scan ID's
        public bool EnableTestId
        {
            get
            {
                return appConfiguration.EnableTestId;
            }

            set
            {
                appConfiguration.EnableTestId = value;
            }
        }

        public double PowerLevelInfo
        {
            get
            {
                return appConfiguration.PowerLevelInfo;
            }

            set
            {
                appConfiguration.PowerLevelInfo = value;
            }
        }

        public double PowerLevelJob
        {
            get
            {
                return appConfiguration.PowerLevelJob;
            }

            set
            {
                appConfiguration.PowerLevelJob = value;
            }
        }

        public double PowerLevelInventory
        {
            get
            {
                return appConfiguration.PowerLevelInventory;
            }

            set
            {
                appConfiguration.PowerLevelInventory = value;
            }
        }

        // Bindable Interface: The actual host to use (modified by the following two options)
        public string Host
        {
            get
            {
                return appConfiguration.Host;
            }

            set
            {
                appConfiguration.Host = value;
            }
        }

        // Bindable Interface: Enter a Custom Host (Only used when option below is Custom)
        public string HostCustom
        {
            get
            {
                return appConfiguration.HostCustom;
            }

            set
            {
                appConfiguration.HostCustom = value;

                // Update the Actual Host If We're Currenty Editing Custom
                if (hostSelect == 2)
                    Host = value;
            }
        }

        // Bindable Interface: Select the Host to Connect to
        public int HostSelect
        {
            get
            {
                return hostSelect;
            }

            set
            {
                hostSelect = value;

                if (hostSelect == 0)
                {
                    Host = appConfiguration.HostMain;
                }
                else if (hostSelect == 1)
                {
                    Host = appConfiguration.HostTest;
                }
                else
                {
                    Host = appConfiguration.HostCustom;
                }

                _ = ExecuteRefreshCompaniesAsync();
            }
        }

        // Jobs Handling
        // =============

        // Request Latest Batch of Jobs
        private async Task ExecuteRefreshJobsAsync()
        {
            ShowSpinner = true;
            try
            {
                await scanJobInventory.Refresh("TEST"); //TODO pipe in scanner ID instead of "TEST"
            }
            catch (Exception ex)
            {
                ReportError(ex);
            }
            ShowSpinner = false;
        }

        // Companies Handling
        // ==================

        // Request Latest Batch of Companies
        private async Task ExecuteRefreshCompaniesAsync()
        {
            ShowSpinner = true;
            try
            {
                await companyInventory.Refresh();
            }
            catch (Exception ex)
            {
                ReportError(ex);
            }
            ShowSpinner = false;
        }

        // Select A Company
        public FarmCompanyInfo SelectedCompany
        {
            get
            {
                return selectedCompany;
            }

            set
            {
                Set(ref selectedCompany, value);
                appConfiguration.CompanyId = selectedCompany.Id;
                appConfiguration.CompanyName = selectedCompany.Name;
            }
        }
    }
}
