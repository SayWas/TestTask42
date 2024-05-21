
# TestTaskDjango Project Documentation

## Introduction
This document provides technical information about the TestTaskDjango project, detailing its architecture, data models, and their relationships.

## System Architecture
The project includes the following main components:
- **Django Models** for managing users, organizations, and contracts.
- **Django REST Framework** for creating APIs.

# Model Descriptions

## Overview
This section provides detailed descriptions of each model within the TestTaskDjango project, including their fields, relationships, and specific functionalities.

## Organization
- **Description**: Serves as the base model for different types of organizations within the system. It is abstract and not used directly but provides common fields for other organization-related models.
- **Fields**:
  - `name`: Text field to store the name of the organization.
- **Relationships**:
  - Inherits to `Subsidiary` and `Contractor`.
- **Responsibilities**: Provides common attributes and functionality for all organizations.

## Subsidiary
- **Description**: Represents a subsidiary organization, inheriting from `Organization`.
- **Fields**:
  - `is_system_owner`: Boolean indicating whether the subsidiary owns the system.
- **Relationships**:
  - Used in `Contract` model to link as `organization_do`.
- **Responsibilities**: Manages attributes specific to subsidiaries and their role within contracts.

## Contractor
- **Description**: Represents a contractor, also inheriting from `Organization`.
- **Fields**:
  - `licensed`: Boolean indicating whether the contractor is licensed to operate.
- **Relationships**:
  - Used in `Contract` model to link as `organization_po`.
- **Responsibilities**: Manages contractor-specific information, including licensing status.

## User
- **Description**: Extends Django's `AbstractUser` to include job titles and organization associations specific to this project.
- **Fields**:
  - `first_name`, `last_name`: User's first and last names.
  - `job_title`: A choice field indicating the user’s role within the organization.
  - `organization`: A `GenericForeignKey` linking to either a `Subsidiary` or `Contractor`.
- **Relationships**:
  - Linked through `ContractRole` to `Contract`.
- **Responsibilities**: Manages user-specific data and roles within the project, facilitating user access and interactions based on their job title and associated organization.

## Contract
- **Description**: Represents a contractual agreement between two organizations.
- **Fields**:
  - `title`: Title of the contract.
  - `start_date`, `end_date`: The duration of the contract.
  - `status`: Current status of the contract.
  - `organization_do`: Link to a `Subsidiary` involved in the contract.
  - `organization_po`: Link to a `Contractor` involved in the contract.
- **Relationships**:
  - Users are linked through `ContractRole` based on their involvement in the contract.
- **Responsibilities**: Manages contract data including tracking status, participants, and validity of contract terms.

## ContractRole
- **Description**: Links users to specific contracts, detailing their roles within those contracts.
- **Fields**:
  - `role`: Specific role of a user within a contract.
- **Relationships**:
  - Links `User` to `Contract`.
- **Responsibilities**: Manages roles of users within contracts, enforcing permissions and access based on roles.


# API and Endpoints Documentation

## Overview
This section outlines the RESTful endpoints available in the TestTaskDjango project, detailing the functionalities, permissions, and expected inputs and outputs.

## Authentication
- **Token Obtain Pair**:
  - `POST /token/`: Obtain a pair of access and refresh JSON web tokens.
- **Token Refresh**:
  - `POST /token/refresh/`: Refresh an access token using a refresh token.

## Contract Endpoints
- **List Contracts**:
  - `GET /contracts/`: Lists all contracts accessible by the authenticated user based on their role and associated organization. General Directors see all contracts, while other users see contracts linked to their organization.
  - **Permissions**: Authenticated users only.

- **Contract Detail**:
  - `GET /contracts/<int:pk>/`: Retrieves detailed information about a specific contract. Access is restricted based on user roles and their relation to the contract.
  - **Permissions**: Authenticated users who are either General Directors or related to the contract through their organization.

- **Manage Contract Users**:
  - `GET /contracts/<int:pk>/manage-users/`: Lists users eligible to be associated with the contract. Restricted to General Directors or those with specific roles in the contract.
  - `POST /contracts/<int:pk>/manage-users/`: Add a user to a contract with a specified role. Validation ensures the user belongs to an organization part of the contract unless added by a General Director.
  - `DELETE /contracts/<int:pk>/manage-users/`: Remove a user and their role from a contract. Requires similar permissions as adding a user.
  - **Permissions**: Authenticated users with enhanced privileges (e.g., General Directors).

## Conclusion
This document is designed to support developers and new users in navigating the project.
