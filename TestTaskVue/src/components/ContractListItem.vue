<template>
  <li class="contract-item" @click="goToContractDetails(contract.id)">
    <div class="contract-header">
      <h2 class="contract-title">{{ contract.title }}</h2>
      <span class="contract-status" :class="`status-${contract.status.toLowerCase()}`">{{ contract.status }}</span>
    </div>
    <div class="contract-details">
      <div class="organization-details">
        <div class="organization-do">Subsidator: {{ contract.organization_do.name }}</div>
        <div class="organization-po">Contractor: {{ contract.organization_po.name }}</div>
      </div>
      <ul class="participant-list">
        <li v-for="user in contract.participants" :key="user.username" class="participant-item">
          {{ user.username }} ({{ user.full_name }})
        </li>
      </ul>
    </div>
  </li>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import type { Contract } from '../api/contracts-api'
import { useRouter } from 'vue-router';

defineProps<{
  contract: Contract
}>();

const router = useRouter();

function goToContractDetails(contractId: number) {
  router.push(`/contracts/${contractId}`);
}
</script>

<style scoped lang="scss">
@import "../assets/styles/mixins.scss";
@import "../assets/styles/variables.scss";

.contract-item {
  padding: 20px;
  margin-bottom: 15px;
  background-color: #fff;
  color: #333;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #ddd;
  @include box-shadow(0 2px 5px rgba(0, 0, 0, 0.1));
  @include transition(background-color 0.3s ease);

  &:hover,
  &:focus {
    background-color: #f5f5f5;
    outline: none;
  }

  .contract-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }

  .contract-title {
    font-weight: 600;
    font-size: 1.2em;
    color: $primary-color;
  }

  .contract-status {
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 500;
    font-size: 0.9em;
    background-color: lighten($secondary-color, 40%);
    color: darken($secondary-color, 20%);

    &.status-pd {
      background-color: #4CAF50;
      color: #fff;
    }

    &.status-up {
      background-color: #f44336;
      color: #fff;
    }
  }

  .organization-details {
    font-size: 0.9em;
    margin-bottom: 10px;
  }

  .participant-list {
    padding: 0;
    list-style: none;
  }

  .participant-item {
    padding: 3px 0;
    font-size: 0.85em;
    color: #666;
  }
}
</style>