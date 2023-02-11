using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron.Models
{
    // Represents a unique item that can be scanned multiple times
    public class IdentifiedItem
        : ViewModels.ViewModelBase
    {
        // The value used when the signal is not specified
        public const double NoSignal = -0.0001;
        // Backing field for <see cref="Identifier"/>
        private string identifier = string.Empty;
        // Backing field for <see cref="SeenCount"/>
        private int seenCount;
        // Backing field for <see cref="FirstSeen"/>
        private DateTime firstSeen;
        // Backing field for LastSeen
        private DateTime lastSeen;
        // Backing field for Signal
        private double normalizedSignal;
        // Backing field for the Source property
        private string source;

        // Displayable details from Server API
        private string crop;
        private string status;
        private string pondLocation;
        private string lotNumber;
        private string rFIDToken;
        private string noOfDaysInPond;
        private string seedingPrompt;
        private string seedingDate;
        private string seederInitials;
        private string transplantPrompt;
        private string transplantDate;
        private string transplanterInitials;
        private string harvestPrompt;
        private string harvestDate;
        private string harvesterInitials;

        // Details used for managing the Display of Data
        private bool showDetails;
        private bool showSummary;
        private string backgroundColor;

        public void Update(FarmRaftInfo raftInfo)
        {
            Crop = raftInfo.cropseededintheraft;
            Status = raftInfo.latestStatus();
            PondLocation = "Pond Location: " + raftInfo.pondLocation;
            LotNumber = "Lot#: " + raftInfo.lotNumber;
            RFID = raftInfo.rFIDToken;
            SeedingPrompt = raftInfo.seedingPrompt();
            SeedingDate = raftInfo.seedingDate;
            SeederInitials = raftInfo.seederInitials;
            TransplantPrompt = raftInfo.transplantPrompt();
            TransplantDate = raftInfo.transplantDate;
            TransplanterInitials = raftInfo.transplanterInitials;
            HarvestPrompt = raftInfo.harvestPrompt();
            HarvestDate = raftInfo.harvestDate;
            HarvesterInitials = raftInfo.harvesterInitials;

            if (raftInfo.noOfDaysInPond >= 0)
            {
                DaysInPond = "Days In Pond: " + raftInfo.noOfDaysInPond;
            }
            else
            {
                DaysInPond = "Days Until Pond: " + (0 - raftInfo.noOfDaysInPond);
            }

            ShowDetails = false;
            ShowSummary = true;
        }
        // Initializes a new instance of the IdentifiedItem class
        // <param name="identifier">The unique identifier of the item</param>
        // <remarks><see cref="Seen(DateTime)"/> should be called each time the item is seen, including the first time</remarks>
        public IdentifiedItem(string identifier)
        {
            this.identifier = identifier;
        }
        // Initializes a new instance of the IdentifiedItem class
        // <param name="identifier">The unique identifier of the item</param>
        // <param name="source"></param>
        // <remarks><see cref="Seen(DateTime)"/> should be called each time the item is seen, including the first time</remarks>
        public IdentifiedItem(string identifier, string source)
        {
            this.identifier = identifier;
            this.source = source;
        }
        // Gets or sets the identifier for the item
        public string Identifier
        {
            get
            {
                return identifier;
            }

            set
            {
                this.Set(ref identifier, value);
            }
        }
        // Gets or sets the number of times this item has been seen
        public int SeenCount
        {
            get
            {
                return seenCount;
            }

            set
            {
                this.Set(ref seenCount, value);
            }
        }
        // Gets or sets the timestamp when the item was first seen
        public DateTime FirstSeen
        {
            get
            {
                return firstSeen;
            }

            set
            {
                this.Set(ref firstSeen, value);
            }
        }
        // Gets or sets the timestamp when the item was last seen
        public DateTime LastSeen
        {
            get
            {
                return lastSeen;
            }

            set
            {
                this.Set(ref lastSeen, value);
            }
        }
        // Gets or sets the received signal strength indication last time the transponder was seen
        public double NormalizedSignal
        {
            get
            {
                return normalizedSignal;
            }

            set
            {
                if (value == NoSignal)
                {
                    value = NoSignal;
                }
                else if (value < 0.0)
                {
                    value = 0.0;
                }
                else if (value > 1.0)
                {
                    value = 1.0;
                }

                this.Set(ref normalizedSignal, value);
            }
        }
        // Gets or sets a text desription for the source of this item
        public string Source
        {
            get
            {
                return source;
            }

            set
            {
                this.Set(ref source, value);
            }
        }
        // Gets or sets the Crop text
        public string Crop
        {
            get
            {
                return crop;
            }

            set
            {
                this.Set(ref crop, value);
            }
        }
        // Gets or sets the Status text
        public string Status
        {
            get
            {
                return status;
            }

            set
            {
                this.Set(ref status, value);
            }
        }
        // Gets or sets the Pond Location text
        public string PondLocation
        {
            get
            {
                return pondLocation;
            }

            set
            {
                this.Set(ref pondLocation, value);
            }
        }
        // Gets or sets the Lot Number text
        public string LotNumber
        {
            get
            {
                return lotNumber;
            }

            set
            {
                this.Set(ref lotNumber, value);
            }
        }
        // Gets or sets the RFID text
        public string RFID
        {
            get
            {
                return rFIDToken;
            }

            set
            {
                this.Set(ref rFIDToken, value);
            }
        }
        // Gets or sets the number of Days In Pond
        public string DaysInPond
        {
            get
            {
                return noOfDaysInPond;
            }

            set
            {
                this.Set(ref noOfDaysInPond, value);
            }
        }
        // Gets or sets the Seeding Prompt text
        public string SeedingPrompt
        {
            get
            {
                return seedingPrompt;
            }

            set
            {
                this.Set(ref seedingPrompt, value);
            }
        }
        // Gets or sets the Seeding Date text
        public string SeedingDate
        {
            get
            {
                return seedingDate;
            }

            set
            {
                this.Set(ref seedingDate, value);
            }
        }
        // Gets or sets the Seeding Initials text
        public string SeederInitials
        {
            get
            {
                return seederInitials;
            }

            set
            {
                this.Set(ref seederInitials, value);
            }
        }
        // Gets or sets the Transplant Prompt text
        public string TransplantPrompt
        {
            get
            {
                return transplantPrompt;
            }

            set
            {
                this.Set(ref transplantPrompt, value);
            }
        }
        // Gets or sets the Transplant Date text
        public string TransplantDate
        {
            get
            {
                return transplantDate;
            }

            set
            {
                this.Set(ref transplantDate, value);
            }
        }
        // Gets or sets the Transplanter Initials text
        public string TransplanterInitials
        {
            get
            {
                return transplanterInitials;
            }

            set
            {
                this.Set(ref transplanterInitials, value);
            }
        }
        // Gets or sets the Harvest Prompt text
        public string HarvestPrompt
        {
            get
            {
                return harvestPrompt;
            }

            set
            {
                this.Set(ref harvestPrompt, value);
            }
        }
        // Gets or sets the Harvest Date text
        public string HarvestDate
        {
            get
            {
                return harvestDate;
            }

            set
            {
                this.Set(ref harvestDate, value);
            }
        }
        // Gets or sets the Harvester Initials text
        public string HarvesterInitials
        {
            get
            {
                return harvesterInitials;
            }

            set
            {
                this.Set(ref harvesterInitials, value);
            }
        }
        // Gets or sets the way this data is presented to the world
        public bool ShowDetails
        {
            get
            {
                return showDetails;
            }

            set
            {
                this.Set(ref showDetails, value);
            }
        }
        public bool ShowSummary
        {
            get
            {
                return showSummary;
            }

            set
            {
                this.Set(ref showSummary, value);
            }
        }
        // Gets or sets the cell background color
        public string BackgroundColor
        {
            get
            {
                return backgroundColor;
            }

            set
            {
                this.Set(ref backgroundColor, value);
            }
        }

        //// <summary>
        //// Marks the item as seen
        //// </summary>
        //// <param name="signal">The RSSI signal seen</param>
        //// <param name="lastSeen">When the item was seen</param>
        //public void Seen(double signal, DateTime lastSeen)
        //{
        //    this.SeenCount += 1;
        //    this.NormalizedSignal = signal;
        //    this.LastSeen = lastSeen == DateTime.MinValue ? DateTime.Now : lastSeen;
        //}
        // Marks the item as seen
        // <param name="lastSeen">When the item was seen</param>
        public void Seen(DateTime lastSeen)
        {
            SeenCount += 1;
            LastSeen = lastSeen == DateTime.MinValue ? DateTime.Now : lastSeen;
            if (FirstSeen == default(DateTime))
            {
                FirstSeen = LastSeen;
            }
        }
        // Returns a string representation of this instance
        // <returns>A string representation of the IdentifiedItem</returns>
        public override string ToString()
        {
            if (normalizedSignal == NoSignal)
            {
                return string.Format(
                    System.Globalization.CultureInfo.CurrentCulture,
                    "{0} {1}",
                    Identifier,
                    SeenCount);
            }
            else
            {
                return string.Format(
                    System.Globalization.CultureInfo.CurrentCulture,
                    "{0} {1} {2}%",
                    Identifier,
                    SeenCount,
                    NormalizedSignal * 100);
            }
        }
    }
}
