Feature: As a user of SVC service
  I want to classify wines using the SVC algorithm

  Scenario: Classify using the SVC algorithm
    Given the SVC service is initialized with a training set
    When I classify the test set using the SVC algorithm
    Then the test set is classified correctly, regarding suitable tolerance
