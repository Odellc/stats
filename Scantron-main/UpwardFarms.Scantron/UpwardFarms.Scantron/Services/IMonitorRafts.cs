
namespace UpwardFarms.Scantron.Services
{
    using System;
    using System.Collections.Generic;
    using System.Text;

    using TechnologySolutions.Rfid;
    // Notifies the progress of a command that returns transponders
    public interface IMonitorRafts
    {
        // Raised for each transponder in the response
        event EventHandler<TranspondersEventArgs> TranspondersReceived;
        // Gets or sets a value indicating whether transponders should be reported
        bool IsEnabled { get; set; }
    }
}
