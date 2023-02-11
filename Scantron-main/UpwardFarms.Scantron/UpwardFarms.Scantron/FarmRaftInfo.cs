using System;
namespace UpwardFarms.Scantron
{
    public class FarmRaftInfo
    {
        public FarmRaftInfo()
        {
            valid = false;
        }

        public FarmRaftInfo(bool is_valid)
        {
            valid = is_valid;
        }

        public string latestStatus()
        {
            if (!valid)
            {
                return "";
            }
            else if ((harvesterInitials != null) && (harvesterInitials.Length > 0))
            {
                return "Harvested: " + harvestDate + " " + harvesterInitials;
            }
            else if ((transplanterInitials != null) && (transplanterInitials.Length > 0))
            {
                return "Transplanted: " + transplantDate + " " + transplanterInitials;
            }
            else if ((seederInitials != null) && (seederInitials.Length > 0))
            {
                return "Seeded: " + seedingDate + " " + seederInitials;
            }
            else if ((seedingDate != null) && (seedingDate.Length > 0))
            {
                return "To Seed: " + seedingDate;
            }
            else
            {
                return "Unused";
            }
        }

        public string seedingPrompt()
        {
            if ((seederInitials != null) && (seederInitials.Length > 0))
            {
                return "Seeded:";
            }
            else
            {
                return "To Seed:";
            }
        }

        public string transplantPrompt()
        {
            if ((transplanterInitials != null) && (transplanterInitials.Length > 0))
            {
                return "Transplanted:";
            }
            else
            {
                return "To Transplant:";
            }
        }

        public string harvestPrompt()
        {
            if ((harvesterInitials != null) && (harvesterInitials.Length > 0))
            {
                return "Harvested:";
            }
            else
            {
                return "To Harvest:";
            }
        }

        public string lotNumber;
        public string rFIDToken;
        public string cropseededintheraft;
        public string pondLocation;
        public string seedingDate;
        public string transplantDate;
        public string harvestDate;
        public int noOfDaysInPond;
        public int rfidOccurrence;
        public string seederInitials;
        public string transplanterInitials;
        public string harvesterInitials;
        public bool valid;
    }
}
