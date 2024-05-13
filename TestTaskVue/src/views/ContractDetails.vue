<template>
    <div class="contract-details-container">
        <h1>Contract Details</h1>
        <div v-if="contract" class="contract-information">
            <h2>{{ contract.title }}</h2>
            <p>Status: <strong>{{ contract.status }}</strong></p>
            <p>Subsidator: {{ contract.organization_do.name }}</p>
            <p>Contractor: {{ contract.organization_po.name }}</p>
            <div class="participants">
                <h3>Participants</h3>
                <div v-if="isEditingAvailable" class="add-participant-form">
                    <select v-model="selectedUser" class="user-select">
                        <option v-for="user in usersChoice" :value="user" :key="user.id">
                            {{ user.full_name }}
                        </option>
                    </select>
                    <select v-model="selectedRole" class="role-select">
                        <option v-for="role in roles" :value="role.value" :key="role.value">
                            {{ role.label }}
                        </option>
                    </select>
                    <button @click="addParticipant">Add</button>
                </div>
                <table class="participants-table">
                    <thead>
                        <tr>
                            <th>Full Name (Username)</th>
                            <th>Contract Role</th>
                            <th>Organization Name</th>
                            <th v-if="isEditingAvailable">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in contract.participants" :key="user.username">
                            <td>{{ user.full_name }} ({{ user.username }})</td>
                            <td>{{ user.contract_role }}</td>
                            <td>{{ user.organization.name }}</td>
                            <td v-if="isEditingAvailable">
                                <button @click="removeParticipant(user)">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <p>Loading contract details...</p>
        </div>
    </div>
</template>


<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { ContractsAPI } from '../api/contracts-api';
import { useUserStore } from '../stores/userStore';
import type { Contract, SelectUser, User } from '../api/contracts-api';

const route = useRoute();
const contract = ref<Contract | null>(null);
const isEditingAvailable = ref(true);
const usersChoice = ref<SelectUser[]>([]);
const selectedUser = ref<SelectUser>();
    const roles = ref([
    { label: 'General Director', value: 'GD' },
    { label: 'Vice Director', value: 'VD' },
    { label: 'Manager', value: 'MN' },
    { label: 'Specialist', value: 'SP' },
    { label: 'Assistant', value: 'AS' }
]);
const selectedRole = ref<string>('');

const addParticipant = async () => {
    if (!selectedUser.value || !selectedRole.value) return;
    const contractId = Number(route.params.id);
    try {
        console.log(selectedUser.value);
        await ContractsAPI.add_user_to_contract(useUserStore().userAccessToken, contractId, selectedUser.value.username, selectedRole.value)
        .then(() => {
            fetchData();
        })
        .catch(error => {
            console.error('Error adding participant:', error);
        });
    } catch (error) {
        console.error('Error adding participant:', error);
    }
};

const roleNameToCode = Object.fromEntries(roles.value.map(role => [role.label, role.value]));
const removeParticipant = async (userToRemove: User) => {
    const contractId = Number(route.params.id);
    const roleCode = roleNameToCode[userToRemove.contract_role]; 
    try {
        await ContractsAPI.delete_user_from_contract(useUserStore().userAccessToken, contractId, userToRemove.username, roleCode)
        .then(() => {
            fetchData();
        })
    } catch (error) {
        console.error('Error removing participant:', error);
    }
};
const fetchData = async () => {
    const contractId = Number(route.params.id);
    try {
        contract.value = await ContractsAPI.get_contract_details(useUserStore().userAccessToken, contractId);
        usersChoice.value = await ContractsAPI.get_available_users(useUserStore().userAccessToken, contractId);
    } catch (error) {
        isEditingAvailable.value = false;
        console.error('Error initializing data:', error);
    }
} 
onMounted(async () => {
    fetchData();
});
</script>


<style scoped lang="scss">
@import "../assets/styles/mixins.scss";
@import "../assets/styles/variables.scss";

.contract-details-container {
    font-family: $font-family-base;
    color: #333;
    background-color: #ffffff;
    padding: 24px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);

    h1 {
        color: $primary-color;
        margin-bottom: 18px;
        font-size: 1.8rem;
    }

    .contract-information {
        background-color: #f2f2f2;
        padding: 20px;
        border-radius: 10px;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);

        h2 {
            color: $secondary-color;
            margin-bottom: 12px;
            font-size: 1.5rem;
        }

        p {
            margin: 4px 0 10px;
            font-size: 1rem;
            line-height: 1.5;

            strong {
                color: $primary-color;
                font-weight: 600;
            }
        }

        .participants {
            margin-top: 20px;

            h3 {
                color: $hover-color;
                font-size: 1.3rem;
                margin-bottom: 10px;
            }

            .add-participant-form {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;

                select, button {
                    flex-grow: 1;
                    padding: 10px;
                    border-radius: 6px;
                    border: 1px solid $input-border-color;
                    background: #fff;
                    &:focus {
                        outline: none;
                        border-color: $focus-color;
                        @include box-shadow('0 0 0 2px rgba($focus-color, 0.25)');
                    }
                }

                button {
                    background-color: $button-background-color;
                    color: white;
                    text-transform: uppercase;
                    transition: background-color 0.3s ease;

                    &:hover {
                        background-color: darken($button-background-color, 10%);
                    }
                }
            }

            .participants-table {
                width: 100%;
                border-collapse: collapse;
                thead {
                    background-color: $secondary-color;
                    color: #fff;
                    th {
                        padding: 12px;
                        text-align: center;
                    }
                }
                tbody {
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    td {
                        padding: 10px;
                        border-top: 1px solid #eee;
                        text-align: center;
                    }
                    button {
                        background-color: $button-background-color;
                        color: white;
                        padding: 6px 12px;
                        border-radius: 4px;
                        border: 1px solid $input-border-color;
                        cursor: pointer;
                        &:hover {
                            background-color: darken($button-background-color, 10%);
                        }
                    }
                }
            }
        }
    }
}

@media (max-width: 768px) {
    .contract-details-container {
        padding: 12px;
        h1, h2, h3 {
            font-size: 1.2rem;
        }

        .participants {
            .add-participant-form {
                flex-direction: column;
                button, select {
                    flex-grow: 1;
                }
            }
        }
    }
}
</style>