<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { onMounted, ref } from 'vue'
import * as d3 from 'd3'
import { feature } from 'topojson-client'
import { ISONumtoISO2, ISONumtoISO3 } from 'country-code-switch'
import BasicCard from '@/components/Cards/BasicCard.vue'

const base_api_url = import.meta.env.VITE_BASE_API_URL
const language = useI18n()
const selectedODD = ref(null)
const selectedColor = ref('#cccccc')
const selectedGoals = ref([])

const odds = ref([
  { id: 1, color: '#E5243B' },
  { id: 2, color: '#DDA63A' },
  { id: 3, color: '#4C9F38' },
  { id: 4, color: '#C5192D' },
  { id: 5, color: '#FF3A21' },
  { id: 6, color: '#26BDE2' },
  { id: 7, color: '#FCC30B' },
  { id: 8, color: '#A21942' },
  { id: 9, color: '#FD6925' },
  { id: 10, color: '#DD1367' },
  { id: 11, color: '#FD9D24' },
  { id: 12, color: '#BF8B2E' },
  { id: 13, color: '#3F7E44' },
  { id: 14, color: '#0A97D9' },
  { id: 15, color: '#56C02B' },
  { id: 16, color: '#00689D' },
  { id: 17, color: '#19486A' },
])

const oddTitles = [
  'Pas de pauvreté',
  'Faim "zéro"',
  'Bonne santé et bien-être',
  'Éducation de qualité',
  'Égalité entre les sexes',
  'Eau propre et assainissement',
  "Énergie propre et d'un coût abordable",
  'Travail décent et croissance économique',
  'Industrie, innovation et infrastructure',
  'Inégalités réduites',
  'Villes et communautés durables',
  'Consommation et production responsables',
  'Mesures relatives à la lutte contre les changements climatiques',
  'Vie aquatique',
  'Vie terrestre',
  'Paix, justice et institutions efficaces',
  'Partenariats pour la réalisation des objectifs',
]

const countryDataByOdd = ref({})

let svg, g, path, projection, zoom
let currentTransform = d3.zoomIdentity
let countries

const generateMockData = () => {
  const mockData = {}
  for (let i = 1; i <= 18; i++) {
    mockData[i] = {}

    mockData[i]['FRA'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['DEU'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['ESP'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['ITA'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['GBR'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['PRT'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['BEL'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['NLD'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['CHE'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['AUT'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['USA'] = 150
    mockData[i]['AFG'] = Math.floor(Math.random() * 100) + 20
    mockData[i]['ARG'] = Math.floor(Math.random() * 100) + 20
  }

  return mockData
}

// const dataFromAPI = async () => {
//   let dataFromApi = {}
//
//   fetch(`${base_api_url}/patents`, {
//     method: 'GET',
//   })
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error('Network response was not ok')
//       }
//       return response.json()
//     })
//     .then((data) => {
//       console.log('File uploaded successfully:', data)
//       dataFromApi = data;
//     })
//     .catch((error) => {
//       console.error('Error uploading file:', error)
//     })
//
//   return dataFromApi;
// };

// Fonction pour sélectionner un ODD
const selectODD = (oddId) => {
  selectedODD.value = oddId
  if (oddId) {
    selectedColor.value = odds.value.find((odd) => odd.id === oddId).color
  } else {
    selectedColor.value = '#cccccc'
  }
  updateMapColors()
}

const updateMapColors = () => {
  console.log('Selected Goals : ' + selectedGoals.value)
  if (!countries) return

  let singleGoal = null
  let multipleGoals = []

  if (selectedGoals.value.length === 1) {
    singleGoal = selectedGoals.value[0] // ID ODD
  } else if (selectedGoals.value.length > 1) {
    multipleGoals = selectedGoals.value // IDs ODD
  }

  countries
    .transition()
    .duration(500)
    .attr('fill', (d) => {
      const countryCode = d.id !== undefined ? ISONumtoISO3(d.id) : null

      if (!countryCode) return '#b7b7b7'

      let value = 0

      if (singleGoal) {
        console.log('Single Goal : ' + singleGoal)
        console.log('Country Code : ' + countryCode)

        const currentData = countryDataByOdd.value[singleGoal]
        value = currentData[countryCode] || 0
        const maxValue = Math.max(...Object.values(currentData))
        const intensity = value / maxValue
        selectedColor.value = odds.value.find((odd) => odd.id === singleGoal).color
        return d3.interpolate('#b7b7b7', selectedColor.value)(intensity)
      } else if (multipleGoals.length > 1) {
        let totalValues = []
        multipleGoals.forEach((goalId) => {
          const data = countryDataByOdd.value[goalId]
          if (data && data[countryCode]) {
            value += data[countryCode]
          }
          for (const code in data) {
            totalValues[code] = (totalValues[code] || 0) + data[code]
          }
        })
        const maxValue = Math.max(...Object.values(totalValues))
        const intensity = value / maxValue
        selectedColor.value = '#6F0474'
        return d3.interpolate('#b7b7b7', selectedColor.value)(intensity)
      } else {
        return '#b7b7b7'
      }
    })
}

const createMap = async () => {
  const width = document.getElementById('world-map').clientWidth
  const height = document.getElementById('world-map').clientHeight

  projection = d3
    .geoMercator()
    .scale(width / 2 / Math.PI)
    .center([0, 40])
    .translate([width / 2, height / 2])

  path = d3.geoPath().projection(projection)

  svg = d3.select('#world-map').append('svg').attr('width', width).attr('height', height)

  g = svg.append('g')

  zoom = d3
    .zoom()
    .scaleExtent([1, 8])
    .on('zoom', (event) => {
      currentTransform = event.transform
      g.attr('transform', currentTransform)

      g.selectAll('.country-label')
        .attr('font-size', () => {
          return `${8 / currentTransform.k > 3 ? 3 : 8 / currentTransform.k}px`
        })
        .style('visibility', currentTransform.k > 2 ? 'visible' : 'hidden')
    })

  svg.call(zoom)

  try {
    const worldData = await d3.json(
      'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json',
    )
    const geojson = feature(worldData, worldData.objects.countries)

    countries = g
      .selectAll('path')
      .data(geojson.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', '#f0f0f0')
      .attr('stroke', '#ccc')
      .attr('stroke-width', 0.5)
      .attr('data-code', (d) => d.id)
      .on('mouseover', function () {
        d3.select(this).attr('stroke-width', 1.5).attr('stroke', '#ccc')
      })
      .on('mouseout', function () {
        d3.select(this).attr('stroke-width', 0.5).attr('stroke', '#ccc')
      })
      .on('click', (event, d) => {
        event.stopPropagation()
        const [[x0, y0], [x1, y1]] = path.bounds(d)

        svg
          .transition()
          .duration(750)
          .call(
            zoom.transform,
            d3.zoomIdentity
              .translate(width / 2, height / 2)
              .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
              .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
          )

        const countryCodeNum = d.id
        const countryCode2 = ISONumtoISO2(countryCodeNum)
        const countryCode3 = ISONumtoISO3(countryCodeNum)
        const countryName = d.properties.name
        const oddId = selectedODD.value
        const count = oddId ? countryDataByOdd.value[oddId] || 0 : 0

        emit('country-selected', {
          codeNum: countryCodeNum,
          code2: countryCode2,
          code3: countryCode3,
          name: countryName,
          oddId: oddId,
          count: count,
        })
      })

    g.selectAll('text')
      .data(geojson.features)
      .enter()
      .append('text')
      .attr('class', 'country-label')
      .attr('x', (d) => path.centroid(d)[0])
      .attr('y', (d) => path.centroid(d)[1])
      .attr('text-anchor', 'middle')
      .attr('fill', '#333')
      .attr('font-size', '8px')
      .attr('font-weight', 'bold')
      .attr('pointer-events', 'none')

    svg.on('click', () => {
      svg.transition().duration(750).call(zoom.transform, d3.zoomIdentity)
    })

    countryDataByOdd.value = generateMockData()
    // countryDataByOdd.value = dataFromAPI();

    updateMapColors()

    const europeBounds = {
      north: 72,
      south: 36,
      east: 40,
      west: -10,
    }

    const northWest = projection([europeBounds.west, europeBounds.north])
    const southEast = projection([europeBounds.east, europeBounds.south])

    if (northWest && southEast) {
      const [x0, y0] = northWest
      const [x1, y1] = southEast

      svg
        .transition()
        .duration(750)
        .call(
          zoom.transform,
          d3.zoomIdentity
            .translate(width / 2, height / 2)
            .scale(Math.min(8, 0.7 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
            .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
        )
    }

    selectODD(2)
  } catch (error) {
    console.error('Erreur lors du chargement des données de la carte:', error)
  }
}

const getSelectedODD = () => {
  return selectedODD.value
}

// watch(selectedGoals, () => {
//   updateMapColors();
// });

onMounted(() => {
  createMap()

  window.addEventListener('resize', () => {
    d3.select('#world-map svg').remove()
    createMap()
  })
})

const getSdgImage = (n) => {
  // Cas particulier : image du bouton "Select All"
  // if (n === 18) return new URL(`../assets/SDG/Français/select_all.png`, import.meta.url).href

  if (language.locale.value === 'fr') {
    return new URL(`../../assets/images/SDG/French/sdg_${n}.png`, import.meta.url).href
  } else if (language.locale.value === 'en') {
    return new URL(`../../assets/images/SDG/English/sdg_${n}.png`, import.meta.url).href
  } else {
    return new URL(`../../assets/images/SDG/Deutsch/sdg_${n}.svg`, import.meta.url).href
  }
}

const toggleSelection = (n) => {
  if (n === 17) {
    // "Select All" toggles all
    if (selectedGoals.value.length < 17) {
      selectedGoals.value = Array.from({ length: 17 }, (_, i) => i + 1)
      updateMapColors()
    } else {
      selectedGoals.value = []
      updateMapColors()
    }
  } else {
    if (selectedGoals.value.includes(n)) {
      selectedGoals.value = selectedGoals.value.filter((g) => g !== n)
      updateMapColors()
    } else {
      selectedGoals.value.push(n)
      updateMapColors()
    }
    console.log('Value 2 :    ' + selectedGoals.value)
    console.log('Size 2 :    ' + selectedGoals.value.length)
    console.log('Value 2 [0] :   ' + selectedGoals.value[0])
  }
}
</script>

<template>
  <div class="map-and-sdg-container">
    <div class="map-container">
      <div id="world-map"></div>
      <div class="legend">
        <div class="legend-title">
          {{
            selectedODD
              ? `ODD #${selectedODD}: ${oddTitles[selectedODD - 1]}`
              : 'Sélectionnez un ODD'
          }}
        </div>
        <div class="legend-scale">
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: '#b7b7b7' }"></div>
            <span>0</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor + '50' }"></div>
            <span>1-50</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor + '70' }"></div>
            <span>50-500</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor + '99' }"></div>
            <span>500-1000</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor }"></div>
            <span>+1000</span>
          </div>
        </div>
      </div>
    </div>

    <div class="sdg-grid">
      <div
        v-for="n in 17"
        :key="n"
        class="sdg-item"
        :class="{ selected: selectedGoals.includes(n) }"
        @click="toggleSelection(n)"
      >
        <img :src="getSdgImage(n)" :alt="`ODD ${n}`" />
      </div>
    </div>
  </div>

  <div class="list-container">
    <BasicCard class="analyze-card"> </BasicCard>
  </div>
</template>

<style scoped>
.list-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 50px;
  height: calc(82vh - (142px * 2));
  width: 100%;
}
.analyze-card {
  width: 80%;
  height: 100%;
}
.map-and-sdg-container {
  display: grid;
  grid-row: auto;
}

.map-container {
  position: relative;
  width: 100%;
  height: calc(90vh - (142px * 2)); /* 142px = size of a SGD item */
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

#world-map {
  width: 100%;
  height: 100%;
}

.legend {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: var(--neutral-low);
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.legend-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.legend-scale {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  border: 1px solid var(--neutral-hight);
}

.sdg-grid {
  display: grid;
  grid-template-columns: repeat(9, minmax(80px, 1fr));
  gap: 10px;
  margin: auto;
  height: 100%;
}

.sdg-item {
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
  height: auto;
  width: auto;
}

.sdg-item.selected {
  transform: scale(0.95);
  opacity: 0.5;
}

.sdg-item img {
  width: 100%;
  height: 100%;
  display: block;
}
</style>
