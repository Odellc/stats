
namespace UpwardFarms.Scantron.Services
{
    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.Threading.Tasks;
    // Provides a method to configure a reader to match a <see cref="Models.InventoryConfiguration"/>
    public interface IInventoryConfigurator
    {
        // Configures Inventory operations to respect the current configuration parameters
        // <returns>
        // The task to configure the reader
        // </returns>
        Task ConfigureAsync();
    }
}
