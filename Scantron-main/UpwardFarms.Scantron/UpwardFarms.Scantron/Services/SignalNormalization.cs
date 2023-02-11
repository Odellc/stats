using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron.Services
{
    // An implementation of <see cref="ISignalNormalization"/>
    public class SignalNormalization
        : ISignalNormalization
    {
        // An expected maximum RSSI signal
        private const int DefaultMaximum = -30;
        // An expected minimum RSSI signal
        private const int DefaultMinimum = -100;
        // The largest RSSI seen since reset
        private int maximumSeen;
        // The smallest RSSI seen since reset
        private int minimumSeen;
        // Initializes a new instance of the SignalNormalization class
        public SignalNormalization()
        {
            this.Reset();
        }
        // Returns a normalized value based on the range of values currently seen
        // <param name="rssi">The value to normalize</param>
        // <returns>The normalized signal</returns>
        public double Normalize(int? rssi)
        {
            if (!rssi.HasValue)
            {
                return 0.0;
            }

            if (rssi > this.maximumSeen)
            {
                this.maximumSeen = rssi.Value;
            }
            else if (rssi < this.minimumSeen)
            {
                this.minimumSeen = rssi.Value;
            }

            return (rssi.Value - this.minimumSeen) / (double)(this.maximumSeen - this.minimumSeen);
        }
        // Resets the normalization
        public void Reset()
        {
            this.maximumSeen = DefaultMaximum;
            this.minimumSeen = DefaultMinimum;
        }
    }
}
