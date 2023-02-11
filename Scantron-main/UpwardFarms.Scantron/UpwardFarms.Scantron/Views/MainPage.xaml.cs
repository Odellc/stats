using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

using UpwardFarms.Scantron.Models;
using UpwardFarms.Scantron.Views;
using UpwardFarms.Scantron.ViewModels;

namespace UpwardFarms.Scantron.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class MainPage : ContentPage
    {
        public MainViewModel TheMainViewModel { get; set; }
        public ScannerViewModel ScannerModel { get; set; }

        public MainPage()
        {
            InitializeComponent();

            this.Appearing += MainPage_Appearing;
            this.Disappearing += MainPage_Disappearing;

            this.BindWithLifecycle(TheMainViewModel = App.ViewModel.TheMainViewModel);
        }

        private void MainPage_Disappearing(object sender, EventArgs e)
        {
            System.Diagnostics.Debug.WriteLine("MainPage. Hidden");
            TheMainViewModel.Hidden();
        }

        private void MainPage_Appearing(object sender, EventArgs e)
        {
            System.Diagnostics.Debug.WriteLine("MainPage. Shown");
            TheMainViewModel.Shown();
        }

        async void OnScannerTapped(object sender, ItemTappedEventArgs args)
        {
            ScannerModel = args.Item as ViewModels.ScannerViewModel;
            if (ScannerModel != null)
            {
                await Task.Run(() =>
                {
                    if (ScannerModel.State == "Connected")
                    {
                        ScannerModel.ExecuteDisconnect();
                    }
                    else
                    {
                        ScannerModel.ExecuteConnect();
                    }
                });
            }
        }

        private Models.IdentifiedItem SelectedRaft { get; set; }
        private FarmRescanJobInfo SelectedJob { get; set; }

        private FarmCompanyInfo SelectedCompany {
            get
            {
                return TheMainViewModel.SelectedCompany;
            }

            set
            {
                TheMainViewModel.SelectedCompany = value;
            }
        }

        void OnRaftTapped(object sender, ItemTappedEventArgs args)
        {
            // Show Details and Highlight the Selected Raft
            if (args.Item != null)
            {
                if (SelectedRaft == args.Item)
                {
                    SelectedRaft = null;
                }
                else
                {
                    SelectedRaft = args.Item as Models.IdentifiedItem;
                    SelectedRaft.BackgroundColor = "#acd36d";
                    SelectedRaft.ShowDetails = true;
                    SelectedRaft.ShowSummary = false;
                }
            }

            // Show Summary for Other Rafts
            foreach (var listItem in this.RaftList.ItemsSource)
            {
                if (listItem != this.SelectedRaft)
                {
                    var raft = listItem as Models.IdentifiedItem;
                    raft.BackgroundColor = "#f0f8f0";
                    raft.ShowDetails = false;
                    raft.ShowSummary = true;
                }
            }
        }

        void OnJobTapped(object sender, ItemTappedEventArgs args)
        {
            if (args.Item != null)
            {
                SelectedJob = args.Item as FarmRescanJobInfo;
                TheMainViewModel.CurJob = SelectedJob.ProdOrderNum;
                TheMainViewModel.CurScanLimit = SelectedJob.NumRafts;
                TheMainViewModel.CurOpMode = MainViewModel.OpMode.JobScan;
            }
            else
            {
                SelectedJob = null;
            }
        }

        async void OnApproveClicked(object sender, EventArgs args)
        {
            // Instruct RaftInventory to post the collection for this Job
            string err = await TheMainViewModel.PostJobValidation();
            if (err.Length < 1)
            {
                TheMainViewModel.CurScanProgress = "Update Complete. Thanks!";
                TheMainViewModel.CurOpMode = MainViewModel.OpMode.JobComplete;
            }
            else
            {
                TheMainViewModel.CurScanProgress = err;
            }
        }

        async void OnManualClicked(object sender, EventArgs args)
        {
            // Manually add an RFID to our list using the contents of the text box
            var inv = App.ViewModel.TheMainViewModel.raftInventory;
            await inv.AddTransponderAsync(ManualRaftId.Text, 0.0f, DateTime.UtcNow);
        }

        void OnDeleteTapped(object sender, EventArgs args)
        {
            var img = ((ImageButton)sender);
            var raft = ((IdentifiedItem)img.CommandParameter);
            TheMainViewModel.DeleteRaft(raft);
        }

        void OnDeleteAllTapped(object sender, EventArgs args)
        {
            TheMainViewModel.ClearRafts();
        }
    }
}