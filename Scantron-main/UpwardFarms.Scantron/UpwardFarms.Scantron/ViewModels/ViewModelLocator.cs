using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace UpwardFarms.Scantron.ViewModels
{
    using TechnologySolutions.Rfid;
    using TechnologySolutions.Rfid.AsciiOperations;
    using TechnologySolutions.Rfid.AsciiProtocol.Extensions;
    using TechnologySolutions.Rfid.AsciiProtocol.Transports;
    // Provides instances of ViewModels for the Views
    public class ViewModelLocator
    {
        // The IOC container
        private readonly Locator locator = Locator.Default;
        // Initializes a new instance of the ViewModelLocator class
        // <remarks>
        // Registers all the required Types with the locator so it can return instances of the ViewModels
        // </remarks>
        public ViewModelLocator()
        {
            var locator = this.locator;
            
            locator.Register<IAsciiTransportsManager, AsciiTransportsManager>();

            if (!locator.IsRegistered<IHostBarcodeHandler>())
            {
                locator.Register<IHostBarcodeHandler, HostBarcodeHandler>();
            }

            locator.Register<MainViewModel>();

            locator.Register<IReaderManager, TslReaderManager>();

            locator.Register<Models.AppConfiguration>();
            locator.Register<Models.InventoryStatistics>(); // none
            locator.Register<Services.IMonitorRafts, Services.MonitorRafts>(); // IReaderOperationInventory
            locator.Register<Services.ISignalNormalization, Services.SignalNormalization>(); // none
            locator.Register<Models.RaftInventory>(); // InventoryStatistics, IMonitorTransponders, ISignalNormalization
            locator.Register<Models.ScanJobInventory>(); // AppConfiguration
            locator.Register<Models.CompanyInventory>(); // AppConfiguration
            locator.Register<Services.IInventoryConfigurator, Services.InventoryConfigurator>(); // IReaderOperationInventory, InventoryConfiguration
            locator.Register<Models.InventoryConfiguration>(); // none
        }
        // Gets the <see cref="ScannersViewModel"/>
        public MainViewModel TheMainViewModel => this.locator.Locate<MainViewModel>();
        // Returns the instance of the specified ViewModel
        // <typeparam name="TViewModel">The type of ViewModel required</typeparam>
        // <returns>The ViewModel instance</returns>
        public TViewModel Locate<TViewModel>()
        {
            return this.locator.Locate<TViewModel>();
        }
    }
}
