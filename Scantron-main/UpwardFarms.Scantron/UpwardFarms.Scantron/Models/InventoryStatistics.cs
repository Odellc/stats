using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron.Models
{
    // Container for statistics relating to the inventory passes
    public class InventoryStatistics
        : ObservableObject
    {
        // Backing field for InventoryMode
        private string inventoryMode = string.Empty;
        // Backing field for CurrentScanSeenCount
        private int currentScanSeenCount;
        // Backing field for CurrentScanUniqueCount
        private int currentScanUniqueCount;
        // Backing field for last scan unique count
        private int lastScanUniqueCount;
        // Backing field for LastScanSeenCount
        private int lastScanSeenCount;
        // Backing field for NumberOfScans
        private int numberOfScans;
        // Backing field for TotalSeenCount
        private int totalSeenCount;
        // Backing field for TotalUniqueCount
        private int totalUniqueCount;
        // Gets or sets the InventoryMode for the inventory
        public string InventoryMode
        {
            get
            {
                return this.inventoryMode;
            }

            set
            {
                this.Set(ref this.inventoryMode, value);
            }
        }
        // Gets or sets the total number of transponders seen in this inventory pass
        public int CurrentScanSeenCount
        {
            get
            {
                return this.currentScanSeenCount;
            }

            set
            {
                this.Set(ref this.currentScanSeenCount, value);
            }
        }
        // Gets or sets the number of new unique identifiers added in this inventory pass
        public int CurrentScanUniqueCount
        {
            get
            {
                return this.currentScanUniqueCount;
            }

            set
            {
                this.Set(ref this.currentScanUniqueCount, value);
            }
        }
        // Gets or sets the total number of transponders since last reset
        public int TotalUniqueCount
        {
            get
            {
                return this.totalUniqueCount;
            }

            set
            {
                this.Set(ref this.totalUniqueCount, value);
            }
        }
        // Gets or sets the total number of identifies seen since the statistics were last reset
        public int TotalSeenCount
        {
            get
            {
                return this.totalSeenCount;
            }

            set
            {
                this.Set(ref this.totalSeenCount, value);
            }
        }
        // Gets or sets the number of inventory passes completed
        public int NumberOfScans
        {
            get
            {
                return this.numberOfScans;
            }

            set
            {
                this.Set(ref this.numberOfScans, value);
            }
        }
        // Gets or sets the number of unique transponders added in the last complete pass
        public int LastScanUniqueCount
        {
            get
            {
                return this.lastScanUniqueCount;
            }

            set
            {
                this.Set(ref this.lastScanUniqueCount, value);
            }
        }
        // Gets or sets the number of transponders seen in the last pass
        public int LastScanSeenCount
        {
            get
            {
                return this.lastScanSeenCount;
            }

            set
            {
                this.Set(ref this.lastScanSeenCount, value);
            }
        }
        // Clears the current statistics
        public void Clear()
        {
            this.CurrentScanSeenCount = 0;
            this.CurrentScanUniqueCount = 0;
            this.InventoryMode = string.Empty;
            this.LastScanSeenCount = 0;
            this.LastScanUniqueCount = 0;
            this.NumberOfScans = 0;
            this.TotalSeenCount = 0;
            this.TotalUniqueCount = 0;
        }
        // Updates the statistics with a partial result
        // <param name="unique">The number of unique transponders seen since the last update</param>
        // <param name="seen">The total number of transponders seen since the last update</param>
        // <param name="endPass">True if this completes the inventory; False otherwise. i.e. to reset the Scan counts</param>
        public void Update(int unique, int seen, bool endPass)
        {
            this.CurrentScanSeenCount += seen;
            this.CurrentScanUniqueCount += unique;
            this.TotalSeenCount += seen;
            this.TotalUniqueCount += unique;

            if (endPass)
            {
                this.EndPass();
            }
        }
        // Copies the current scan values to the last scan values.
        // Resets the current scan values and increments the scan count
        public void EndPass()
        {
            this.LastScanSeenCount = this.CurrentScanSeenCount;
            this.LastScanUniqueCount = this.CurrentScanUniqueCount;
            this.CurrentScanSeenCount = 0;
            this.CurrentScanUniqueCount = 0;
            this.NumberOfScans += 1;
        }
    }
}
