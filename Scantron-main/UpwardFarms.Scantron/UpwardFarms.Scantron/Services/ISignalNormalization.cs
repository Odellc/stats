using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron.Services
{
    // Provides methods to normalize a signal
    public interface ISignalNormalization
    {
        // Clear history of previous readings
        void Reset();
        // Returns a normalized version of the signal
        // <param name="rssi">The received signal strength</param>
        // <returns>The normalized signal</returns>
        double Normalize(int? rssi);
    }
}
