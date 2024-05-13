import { DefaultAPIInstance } from '@/api'

export interface Organization {
  id: number
  name: string
}

export interface Subsidiary extends Organization {
  is_system_owner: boolean
}

export interface Contractor extends Organization {
  licensed: boolean
}

export interface User {
  username: string
  full_name: string
  contract_role: string
  organization: Contractor | Subsidiary
}

export interface SelectUser {
  id: number
  username: string
  full_name: string
}

export interface Contract {
  id: number
  title: string
  start_date: string
  end_date: string
  status: 'PD' | 'UP'
  organization_do: Subsidiary
  organization_po: Contractor
  participants: User[]
}

export interface ManageUserResponse {
  message: string
}

export const ContractsAPI = {
  /**
   * Retrieves a list of all contracts.
   * @param userAccessToken - The user's access token for authentication.
   * @returns A Promise resolving to an array of Contract objects.
   * @throws Will throw an error if the request fails or if the response is not as expected.
   */
  async get_contracts(userAccessToken: string): Promise<Contract[]> {
    try {
      const response = await DefaultAPIInstance.get<Contract[]>('/contracts/', {
        headers: {
          Authorization: `Bearer ${userAccessToken}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching contracts:', error)
      throw new Error('Failed to fetch contracts')
    }
  },
  /**
   * Retrieves details of a specific contract.
   * @param userAccessToken - The user's access token.
   * @param contractId - The unique identifier of the contract.
   * @returns A Promise resolving to a Contract object.
   * @throws Will throw an error if the request fails or the contract details are not retrieved.
   */
  async get_contract_details(userAccessToken: string, contractId: number): Promise<Contract> {
    try {
      const response = await DefaultAPIInstance.get<Contract>(`/contracts/${contractId}/`, {
        headers: {
          Authorization: `Bearer ${userAccessToken}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching contract details:', error)
      throw new Error('Failed to fetch contract details')
    }
  },
  /**
   * Retrieves a list of users associated with a specific contract.
   * @param userAccessToken - The user's access token.
   * @param contractId - The contract ID for which to retrieve users.
   * @returns A Promise resolving to an array of User objects.
   * @throws Will throw an error if the request fails or the user list is not retrieved.
   */
  async get_available_users(userAccessToken: string, contractId: number): Promise<SelectUser[]> {
    try {
      const response = await DefaultAPIInstance.get<SelectUser[]>(
        `/contracts/${contractId}/manage-users/`,
        {
          headers: {
            Authorization: `Bearer ${userAccessToken}`
          }
        }
      )
      if (response.status === 200) {
        return response.data
      } else {
        throw new Error(`Unexpected response status: ${response.status}`)
      }
    } catch (error) {
      console.error('Error fetching users:', error)
      throw new Error('Failed to fetch users')
    }
  },
  /**
   * Removes a user from a contract.
   * @param userAccessToken - The user's access token.
   * @param contractId - The ID of the contract from which to remove the user.
   * @param userId - The ID of the user to remove.
   * @returns A Promise resolving to a ManageUserResponse indicating success or failure.
   * @throws Will throw an error if the removal request fails.
   */
  async delete_user_from_contract(
    userAccessToken: string,
    contractId: number,
    usernameToDelete: string,
    roleToRemove: string
  ): Promise<ManageUserResponse> {
    try {
      const response = await DefaultAPIInstance.delete<ManageUserResponse>(
        `/contracts/${contractId}/manage-users/`,
        {
          data: { username: usernameToDelete, role: roleToRemove },
          headers: {
            Authorization: `Bearer ${userAccessToken}`
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('Error removing user from contract:', error)
      throw new Error('Failed to remove user from contract')
    }
  },
  /**
   * Adds a user to a contract.
   * @param userAccessToken - The user's access token.
   * @param contractId - The ID of the contract to which to add the user.
   * @param userId - The ID of the user to add.
   * @returns A Promise resolving to a ManageUserResponse indicating success or failure.
   * @throws Will throw an error if the addition request fails.
   */
  async add_user_to_contract(
    userAccessToken: string,
    contractId: number,
    usernameToAdd: string,
    roleToAdd: string
  ): Promise<ManageUserResponse> {
    try {
      const response = await DefaultAPIInstance.post<ManageUserResponse>(
        `/contracts/${contractId}/manage-users/`,
        {
          username: usernameToAdd,
          role: roleToAdd
        },
        {
          headers: {
            Authorization: `Bearer ${userAccessToken}`
          }
        }
      )
      return response.data
    } catch (error) {
      console.error('Error adding user to contract:', error)
      throw new Error('Failed to add user to contract')
    }
  }
}
