using System;
namespace UpwardFarms.Scantron
{
    public class FarmRescanJobInfo
        : ViewModels.ViewModelBase
    {
        public FarmRescanJobInfo()
        {
            valid = false;
        }

        public FarmRescanJobInfo(string orderNum, int numRafts)
        {
            this.prodOrderNo = orderNum;
            this.noOfRafts = numRafts;
            this.valid = true;
        }

        public string prodOrderNo;
        public int noOfRafts;
        public bool valid;

        public string ProdOrderNum
        {
            get
            {
                return prodOrderNo;
            }

            set
            {
                this.Set(ref prodOrderNo, value);
            }
        }

        public int NumRafts
        {
            get
            {
                return noOfRafts;
            }

            set
            {
                this.Set(ref noOfRafts, value);
            }
        }
    }
}
