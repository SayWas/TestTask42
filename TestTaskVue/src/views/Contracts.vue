<template>
  <div class="contracts-container">
    <h1>Contracts Overview</h1>
    <ul>
      <ContractListItem v-for="contract in contracts" :key="contract.id" :contract="contract" />
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ContractsAPI } from '../api/contracts-api';
import { useUserStore } from '../stores/userStore';
import ContractListItem from '@/components/ContractListItem.vue';
import type { Contract } from '../api/contracts-api';

const contracts = ref<Contract[]>([]);

onMounted(async () => {
  try {
    contracts.value = await ContractsAPI.get_contracts(useUserStore().userAccessToken);
  } catch (error) {
    console.error('Failed to fetch contracts', error);
  }
});
</script>

<style scoped lang="scss">
@import "../assets/styles/variables.scss";
@import "../assets/styles/mixins.scss";

.contracts-container {
  font-family: $font-family-base;
  display: flex;
  flex-direction: column;
  padding: 20px;

  h1 {
    color: $primary-color;
    margin-bottom: 20px;
    font-size: 2em;
  }

  ul {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 0;
    list-style: none;
    margin: 0;
  }
}

.contract-item {
  padding: 20px;
  margin-bottom: 15px;
  min-width: 300px;
  flex: 1 1 40%;
  background-color: #fff;
  color: #333;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;

  &:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
    background-color: #f5f5f5;
  }
}
</style>
