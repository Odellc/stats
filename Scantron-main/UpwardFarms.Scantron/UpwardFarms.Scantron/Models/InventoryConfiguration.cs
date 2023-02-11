using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron.Models
{
    // A representation of the required reader Inventory parameter configuration
    public class InventoryConfiguration
        : ObservableObject
    {
        // Backing field for <see cref="OutputPower"/>
        private Tracked<int> outputPower;
        private Tracked<bool> includeChannelFrequency;
        private Tracked<bool> includeChecksum;
        private Tracked<bool> includeDateTime;
        private Tracked<bool> includeEpc;
        private Tracked<bool> includeIndex;
        private Tracked<bool> includePc;
        private Tracked<bool> includePhase;
        private Tracked<bool> includeRssi;
        // Backing field for <see cref="MaximumPower"/>
        private int maximumPower;
        // Backing field for <see cref="MinimumPower"/>
        private int minimumPower;

        public InventoryConfiguration()
        {
            this.outputPower = new Tracked<int>();
            this.includeChannelFrequency = new Tracked<bool>();
            this.includeChecksum = new Tracked<bool>();
            this.includeDateTime = new Tracked<bool>();
            this.includeEpc = new Tracked<bool>();
            this.includeIndex = new Tracked<bool>();
            this.includePc = new Tracked<bool>();
            this.includePhase = new Tracked<bool>();
            this.includeRssi = new Tracked<bool>();

            // EPC is required for unique transponder count to work
            this.IncludeEpc = true;

            // Set Acceptable Power Range (And Current Output Power)
            this.MinimumPower = 10;
            this.OutputPower  = 20;
            this.MaximumPower = 29;

            // Set Other Default Traits:
            this.IncludeRssi = true;
        }
        // Gets or sets a value indicating whether channel frequency at which the transponder was inventoried should be reported
        public bool IncludeChannelFrequency
        {
            get
            {
                return this.includeChannelFrequency.value;
            }

            set
            {
                this.Set(ref this.includeChannelFrequency.value, value);
            }
        }
        // Gets or sets a value indicating whether the checksum of the transponder should be reported
        public bool IncludeChecksum
        {
            get
            {
                return this.includeChecksum.value;
            }

            set
            {
                this.Set(ref this.includeChecksum.value, value);
            }
        }
        // Gets or sets a value indicating whether the timestamp of the inventory should be reported
        public bool IncludeDateTime
        {
            get
            {
                return this.includeDateTime.value;
            }

            set
            {
                this.Set(ref this.includeDateTime.value, value);
            }
        }
        // Gets or sets a value indicating whether the EPC of the transponder should be reported
        public bool IncludeEpc
        {
            get
            {
                return this.includeEpc.value;
            }

            set
            {
                this.Set(ref this.includeEpc.value, value);
            }
        }
        // Gets or sets a value indicating whether the index of the transponder (per inventory) should be reported
        public bool IncludeIndex
        {
            get
            {
                return this.includeIndex.value;
            }

            set
            {
                this.Set(ref this.includeIndex.value, value);
            }
        }        
        // Gets or sets a value indicating whether the RSSI should be reported
        public bool IncludeRssi
        {
            get
            {
                return this.includeRssi.value;
            }

            set
            {
                this.Set(ref this.includeRssi.value, value);
            }
        }
        // Gets or sets the maximum output power of the connected reader
        public int MaximumPower
        {
            get
            {
                return this.maximumPower;
            }

            set
            {
                this.Set(ref this.maximumPower, (int)value);
            }
        }
        // Gets or sets the minimum output power of the connected reader
        public int MinimumPower
        {
            get
            {
                return this.minimumPower;
            }

            set
            {
                this.Set(ref this.minimumPower, (int)value);
            }
        }
        // Gets or sets the antenna output power
        public int OutputPower
        {
            get
            {
                return this.outputPower.value;
            }

            set
            {
                this.Set(ref this.outputPower.value, value);
            }
        }
        // Gets a value indicating whether the configuration values are different since the last update
        public bool IsChanged
        {
            get
            {
                return this.outputPower.IsChanged |
                    this.includeChannelFrequency.IsChanged |
                    this.includeChecksum.IsChanged |
                    this.includeDateTime.IsChanged |
                    this.includeEpc.IsChanged |
                    this.includeIndex.IsChanged |
                    this.includePc.IsChanged |
                    this.includePhase.IsChanged |
                    this.includeRssi.IsChanged;
            }
        }
        // Clears <see cref="IsChanged"/> by updating the original values to match the current values
        public void UpdateAll()
        {
            this.outputPower.Update();
            this.includeChannelFrequency.Update();
            this.includeChecksum.Update();
            this.includeDateTime.Update();
            this.includeEpc.Update();
            this.includeIndex.Update();
            this.includePc.Update();
            this.includePhase.Update();
            this.includeRssi.Update();
        }
        // Simple class to track the change to a backing field
        // <typeparam name="TValue">The type of the backing field</typeparam>
        private struct Tracked<TValue>
        {
            // Holds the original (or <see cref="Update"/>d) value of the field
            private TValue original;
            // Exposes the current value for use with the normal ViewModel Set pattern
            public TValue value;
            // Updates the original value to match the current value so the field is no longer changed
            public void Update()
            {
                this.original = this.value;
            }
            // Gets a value indicating whether the field value has changed since the last update
            public bool IsChanged
            {
                get
                {
                    return !object.Equals(this.original, this.value);
                }
            }
        }
    }
}
