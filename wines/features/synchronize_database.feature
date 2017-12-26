Feature: As an operator of the datastore
  I want the datastore to set its state by
  reading all entries of the distributed log
  and applying them.

  @needs_state_reset
  @log_synchronization
  Scenario: Synchronize log entries
    When I log some create and delete entries
    Then the create entries can be received
      And the delete entries cannot be received
