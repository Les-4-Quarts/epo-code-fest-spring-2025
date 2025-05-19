<template>
  <div class="explore-container">
   <div class="explore-content">
      <div class="map-section">
        <div class="map-wrapper">
          <MapODD ref="mapODD"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { ref, onMounted } from 'vue';
// import { useRouter } from 'vue-router';
import MapODD from '@/components/Map/MapODD.vue';

export default {
  name: 'ExploreView',
  components: {
    MapODD
  },
  // setup() {
  //   const router = useRouter();
  //   const mapODD = ref(null);
  //   const selectedCountry = ref(null);
  //   const selectedRegion = ref('');
  //   const selectedYear = ref('');
  //   const selectedTypes = ref([]);
  //   const initiatives = ref([]);
  //
  //
  //   const oddColors = {
  //     1: '#E5243B',
  //     2: '#DDA63A',
  //     3: '#4C9F38',
  //     4: '#C5192D',
  //     5: '#FF3A21',
  //     6: '#26BDE2',
  //     7: '#FCC30B',
  //     8: '#A21942',
  //     9: '#FD6925',
  //     10: '#DD1367',
  //     11: '#FD9D24',
  //     12: '#BF8B2E',
  //     13: '#3F7E44',
  //     14: '#0A97D9',
  //     15: '#56C02B',
  //     16: '#00689D',
  //     17: '#19486A'
  //   };
  //   const getODDColor = (oddId) => {
  //     return oddColors[oddId] || '#cccccc';
  //   };
  //
  //   const onCountrySelected = (country) => {
  //     selectedCountry.value = {
  //       codeNumeric: country.codeNum,
  //       codeAlpha2: country.code2,
  //       codeAlpha3: country.code3,
  //       name: country.name,
  //       numberPatents: country.count
  //     };
  //
  //     loadInitiatives(country.code);
  //   };
  //
  //
  //
  //   const applyFilters = () => {
  //     console.log('Filtres appliqués:', {
  //       region: selectedRegion.value,
  //       year: selectedYear.value,
  //       types: selectedTypes.value
  //     });
  //
  //     selectedCountry.value = null;
  //     initiatives.value = [];
  //   };
  //
  //   const viewCountryDetails = (countryCode) => {
  //     router.push(`/country/${countryCode}`);
  //   };
  //
  //   const viewInitiativeDetails = (initiativeId) => {
  //     router.push(`/initiative/${initiativeId}`);
  //   };
  //
  //   const formatNumber = (value) => {
  //     return new Intl.NumberFormat().format(value);
  //   };
  //
  //   const formatCurrency = (value) => {
  //     return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(value);
  //   };
  //
  //   onMounted(() => {
  //   });
  //
  //   return {
  //     mapODD,
  //     selectedCountry,
  //     selectedRegion,
  //     selectedYear,
  //     selectedTypes,
  //     initiatives,
  //     onCountrySelected,
  //     applyFilters,
  //     viewCountryDetails,
  //     viewInitiativeDetails,
  //     getODDColor,
  //     formatNumber,
  //     formatCurrency
  //   };
  // },
  // filters: {
  //   formatNumber(value) {
  //     return new Intl.NumberFormat().format(value);
  //   },
  //   formatCurrency(value) {
  //     return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(value);
  //   }
  // }
};
</script>

<style scoped>
.explore-container {
  width: 100%;
  max-width: 1400px;
  height: 100%;
  margin: 0 auto;
  padding: 20px;
}

.explore-content {
  width: 1400px;
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
}

.map-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.map-wrapper {
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.country-details h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.5rem;
}
</style>
