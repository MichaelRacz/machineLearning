Feature: As a maintainer of the wine dataset
  I want to create new wine records and add
  them to the dataset.

  Background:
    Given I have access to the Wine API

  Scenario: Create a new wine record
    Given I have a valid wine record
    When I POST it to the create_wine endpoint
    Then I receive the id of created wine record
      And the HTTP status code is "201"
      And I GET the record from the get_wine endpoint

  Scenario: Create a new wine record with minimum wine property values
    Given I have a valid wine record
      And All wine record properties are set to "0"
    When I POST it to the create_wine endpoint
    Then I receive the id of created wine record
      And the HTTP status code is "201"

  Scenario: Pass a wine record without a wine class
    Given I have a wine record without a wine class
    When I POST it to the create_wine endpoint
    Then I receive a validation error indicating a missing required property
      And the HTTP status code is "400"

  Scenario: Pass a wine record without a wine
    Given I have a wine record without a wine
    When I POST it to the create_wine endpoint
    Then I receive a validation error indicating a missing required property
      And the HTTP status code is "400"

  Scenario Outline: Pass a wine record with a wine with a missing property
    Given I have a wine record with a wine without property "<wine_property>"
    When I POST it to the create_wine endpoint
    Then I receive a validation error indicating a missing required property
      And the HTTP status code is "400"
    Examples: Wine properties
      | wine_property |
      | alcohol |
      | malic_acid |
      | ash |
      | alcalinity_of_ash |
      | magnesium |
      | total_phenols |
      | flavanoids |
      | nonflavanoid_phenols |
      | proanthocyanins |
      | color_intensity |
      | hue |
      | odxxx_of_diluted_wines |
      | proline |

  Scenario Outline: Pass valid wine class
    Given I have a wine record with a wine class "<wine_class>"
    When I POST it to the create_wine endpoint
    Then I receive the id of created wine record
      And the HTTP status code is "201"
    Examples: Valid wine classes
      | wine_class |
      | 1 |
      | 2 |
      | 3 |

  Scenario Outline: Pass invalid wine class
    Given I have a wine record with a wine class "<wine_class>"
    When I POST it to the create_wine endpoint
    Then I receive a validation error indicating an invalid value for wine class
      And the HTTP status code is "400"
    Examples: Invalid wine classes
      | wine_class |
      | 0 |
      | 4 |
      | invalid |

  Scenario: Create a new wine record with invalid wine property values
    Given I have a valid wine record
      And All wine record properties are set to "-1"
    When I POST it to the create_wine endpoint
    Then I receive a validation error for all properties indicating an invalid value
      And the HTTP status code is "400"
