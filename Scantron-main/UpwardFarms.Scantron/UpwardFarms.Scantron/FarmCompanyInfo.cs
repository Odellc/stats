using System;
namespace UpwardFarms.Scantron
{
    public class FarmCompanyInfo
        : ViewModels.ViewModelBase
    {
        public FarmCompanyInfo()
        {
            valid = false;
        }

        public FarmCompanyInfo(string name, string id)
        {
            this.name = name;
            this.id = id;
            this.valid = true;
        }

        public string name;
        public string id;
        public bool valid;

        public string Name
        {
            get
            {
                return name;
            }

            set
            {
                this.Set(ref name, value);
            }
        }

        public string Id
        {
            get
            {
                return id;
            }

            set
            {
                this.Set(ref id, value);
            }
        }
    }
}
