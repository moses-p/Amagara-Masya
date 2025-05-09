<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <div v-for="group in groups" :key="group.id">
        {{ group.name }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      groups: [],
      loading: true,
      error: null
    };
  },
  computed: {
    uniqueGroups() {
      if (!this.groups || !Array.isArray(this.groups)) {
        return [];
      }
      return this.groups;
    }
  },
  async mounted() {
    await this.fetchGroups();
  },
  methods: {
    async fetchGroups() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No authentication token found');
        }

        const response = await axios.get('http://localhost:8000/api/core/groups/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }); // API URL points to Django backend
        this.groups = response.data.results || response.data;
      } catch (error) {
        console.error('Error fetching groups:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style>
  /* No changes to style section */
</style> 