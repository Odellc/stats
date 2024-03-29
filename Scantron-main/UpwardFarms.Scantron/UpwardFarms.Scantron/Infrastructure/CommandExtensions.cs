﻿using System;
using System.Collections.Generic;
using System.Text;

namespace UpwardFarms.Scantron
{
    // Extension methods for commands.
    public static class CommandExtensions
    {
        // Assumes command is a <see cref="RelayCommand"/> and calls <see cref="RelayCommand.RaiseCanExecuteChanged"/>
        // <param name="command">The command to raise <see cref="System.Windows.Input.ICommand.CanExecuteChanged"/></param>
        public static void RefreshCanExecute(this System.Windows.Input.ICommand command)
        {
            (command as RelayCommand)?.RaiseCanExecuteChanged();
        }
    }
}
