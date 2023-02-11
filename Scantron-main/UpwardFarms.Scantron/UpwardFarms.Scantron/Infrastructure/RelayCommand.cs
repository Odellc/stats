using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Input;

namespace UpwardFarms.Scantron
{
    // Defines an System.Windows.Input.ICommand implementation that wraps a System.Action.
    public class RelayCommand 
        : ICommand
    {
        // The action to perform to execute the command
        private readonly Action<object> execute;
        // The function that returns a value indicating whether the command can execute
        private readonly Func<object, bool> canExecute;

        public RelayCommand(Action<object> execute)
            : this(execute, null)
        {
        }

        public RelayCommand(Action execute)
            : this(execute, null)
        {
        }

        public RelayCommand(Action<object> execute, Func<object, bool> canExecute)
        {
            if (execute == null)
            {
                throw new ArgumentNullException("execute");
            }

            this.canExecute = canExecute ?? new Func<object, bool>((parameter) => { return true; });
            this.execute = execute;
        }
        // Initializes a new instance of the RelayCommand class
        // <param name="execute">The action to perform to execute the command</param>
        // <param name="canExecute">A function that returns a bool indicating whether the command can be execute</param>
        public RelayCommand(Action execute, Func<bool> canExecute)
            : this((parameter) => { execute(); }, (parameter) => { return canExecute == null ? true : canExecute(); })
        {
        }
        // Should be raised when CanExecute should be evaluated
        public event EventHandler CanExecuteChanged;
        // Returns a <see cref="bool"/> indicating if the Command can be executed with the given parameter.
        // <param name="parameter">An System.Object used as parameter to determine if the Command can be executed.</param>
        // <returns>true if the Command can be executed, false otherwise.</returns>
        // <remarks>
        // If no canExecute parameter was passed to the Command constructor, this method always returns true.
        // If the Command was created with non-generic execute parameter, the parameter of this method is ignored.
        // </remarks>
        public bool CanExecute(object parameter)
        {
            return this.canExecute(parameter);
        }
        // Sends a <see cref="CanExecuteChanged"/>
        public void RaiseCanExecuteChanged()
        {
            this.CanExecuteChanged?.Invoke(this, EventArgs.Empty);
        }
        // Invokes the execute Action
        // <param name="parameter">An System.Object used as parameter for the execute Action.</param>
        // <remarks>
        // If the Command was created with non-generic execute parameter, the parameter of this method is ignored.
        // </remarks>
        public void Execute(object parameter)
        {
            if (this.CanExecute(parameter))
            {
                this.execute(parameter);
            }
        }
    }
}
