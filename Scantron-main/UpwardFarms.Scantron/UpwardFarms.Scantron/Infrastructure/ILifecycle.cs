using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron
{
    // When implemented by a view provides methods to a ViewModel that are called for view events
    public interface ILifecycle
    {
        // Called when the view is displayed
        void Shown();
        // Called when the view is hidden
        void Hidden();
    }
}
