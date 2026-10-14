# Issues Identified and Fixed

This document records the issues found while running Bandit, Pylint, and
Flake8 on `helpdesk_system.py` for the Helpdesk Ticket Management
System.

## Issues Identified and Fixed

  ----------------------------------------------------------------------------------------------------------------------
  Issue           Type           Location                Description                Fix Approach
  --------------- -------------- ----------------------- -------------------------- ------------------------------------
  Hardcoded       Security ---   Initial version         A password was stored      Read the administrator password from
  administrator   Low                                    directly in the source     the `HELPDESK_ADMIN_PASSWORD`
  password                                               code, which could expose   environment variable instead of
                                                         credentials if the file    hardcoding it.
                                                         were shared.               

  Unsafe          Security ---   `ping_user_machine()`   The initial implementation Removed shell-based execution and
  subprocess      Low                                    used `shell=True` and      used safer argument handling. The
  execution                                              constructed a shell        final implementation checks the
                                                         command using the supplied hostname and uses
                                                         hostname. This can create  `socket.getaddrinfo()` to check name
                                                         command-injection risk.    resolution without launching a shell
                                                                                    command.

  Unsafe or       Security ---   Initial                 The initial implementation Removed the subprocess-based
  partial         Low            `ping_user_machine()`   relied on a partial        implementation, eliminating the
  executable path                                        executable path when       partial executable path issue.
                                                         starting `ping`.           

  Potentially     Security ---   Imports in the initial  The initial version        Removed the unused subprocess-based
  risky           Low            version                 imported `subprocess` for  approach from the final
  subprocess                                             the hostname check.        implementation.
  import                                                                            

  Mutable default Bug / Code     `raise_ticket()`        A list used as a default   Changed the default to `None` and
  argument        quality                                argument could be shared   initialized a new list inside the
                                                         between function calls.    function.

  Invalid urgency Input          `raise_ticket()` and    Urgency values outside the Convert urgency to an integer and
  values          validation     `main()`                permitted range could be   require a value from 1 through 5;
                                                         accepted or cause          handle invalid input in the
                                                         unexpected behavior.       demonstration.

  Missing ticket  Bug / Code     `assign_ticket()`,      Operations on a            Check whether the ticket ID exists
  checks          quality        `add_note()`,           nonexistent ticket could   before changing or closing a ticket;
                                 `close_ticket()`        raise an error or behave   return `False` when it does not
                                                         unexpectedly.              exist.

  Broad or silent Code quality   Initial `add_note()`    A broad or silent          Check ticket existence explicitly
  exception                      implementation          exception-handling pattern rather than relying on a bare
  handling                                               can hide the cause of an   exception and silent `pass`.
                                                         error.                     

  Missing module  Code quality   Module and functions    The initial code lacked    Added a module docstring and
  and function                                           module and function        docstrings to the functions.
  documentation                                          docstrings, reducing       
                                                         readability and            
                                                         maintainability.           

  Non-standard    Style          High-priority ticket    The initial function name  Renamed it to
  function naming                lookup                  `unresolvedHighPriority`   `unresolved_high_priority()`.
                                                         did not follow Python's    
                                                         `snake_case` convention.   

  Constant naming Style          Ticket counter          Pylint flagged the name    Kept the counter as mutable state
  convention                                             `ticket_counter` as a      and reviewed the naming warning
                                                         constant-style naming      against its actual role.
                                                         issue in the earlier       
                                                         version.                   

  Long lines and  Style          Multiple locations      Flake8 reported lines      Wrapped long expressions and
  blank-line                                             exceeding the configured   adjusted spacing to follow Flake8's
  spacing                                                length and incorrect       formatting requirements.
                                                         blank-line spacing.        

  Unsafe file     Code quality   `save_tickets()`        The initial code opened a  Used
  handling                                               file without a context     `with open(..., encoding="utf-8")`
                                                         manager or explicit text   so the file is closed reliably and
                                                         encoding.                  the encoding is explicit.

  Unused          Code quality   Initial and             Static analysis identified Removed unused items and retained
  variables and                  intermediate versions   unused variables or        only imports needed by the final
  imports                                                imports in earlier         implementation.
                                                         versions.                  
  ----------------------------------------------------------------------------------------------------------------------

## Final Static Analysis Results

The final checks were run against `helpdesk_system.py` after the
changes.

  Tool                 Final result
  -------------------- ------------------------------------------
  Bandit               No issues identified
  Pylint               9.70/10
  Flake8               No output; no formatting issues reported
  Python compilation   Completed without errors

## Summary

The Helpdesk Ticket Management System was updated to improve security,
input validation, error handling, readability, and formatting. The final
version avoids shell-based subprocess execution for hostname checking,
reads the administrator password from an environment variable, validates
urgency values, checks ticket IDs before operations, and uses safer file
handling.

The results above describe the final runs captured during the lab work.
If the code is changed again, rerun all four checks and update this
report if the results change.
