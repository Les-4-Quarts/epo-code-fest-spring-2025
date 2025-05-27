<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { computed, onMounted, ref, watch } from 'vue'
import * as d3 from 'd3'
import { feature } from 'topojson-client'
import { ISONumtoISO3, ISO3toISO2 } from 'country-code-switch'
import type { Objects, Topology } from 'topojson-specification'
import type { GeoJsonProperties } from 'geojson'
import type { Stats } from '@/types/Stats'

const base_api_url = import.meta.env.VITE_BASE_API_URL
const { t } = useI18n()
const selectedSdgTitle = ref('All selected')
const selectedColor = ref('#cccccc')
const statsData = ref<Stats | null>(null)
const selectedGoals = ref<number[]>([])

const props = defineProps({
  selectedGoals: {
    type: Array as () => number[],
    default: () => ref<number[]>([]),
  },
})

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

let oddTitles = [
  t('sdg.1'),
  t('sdg.2'),
  t('sdg.3'),
  t('sdg.4'),
  t('sdg.5'),
  t('sdg.6'),
  t('sdg.7'),
  t('sdg.8'),
  t('sdg.9'),
  t('sdg.10'),
  t('sdg.11'),
  t('sdg.12'),
  t('sdg.13'),
  t('sdg.14'),
  t('sdg.15'),
  t('sdg.16'),
  t('sdg.17'),
]

const countryDataByOdd = ref<Record<number, Record<string, number>>>({})

async function getPatentStats(selectedGoals: number[]) {
  fetch(
    `${base_api_url}/patents/stats?sdgs=${selectedGoals.filter((n: number) => n != 18).join(',')}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    },
  )
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      return response.json()
    })
    .then((data: Stats) => {
      statsData.value = data
      countryDataByOdd.value = data.stats || {}
      updateMapColors()
    })
    .catch((error) => {
      console.error('There was a problem with the fetch operation:', error)
    })
}
getPatentStats(props.selectedGoals)

watch(
  () => props.selectedGoals,
  (newSelectedGoals) => {
    selectedGoals.value = newSelectedGoals
  },
  { immediate: true, deep: true }, // Watch for changes in the array
)

watch(
  () => selectedGoals.value,
  (newSelectedGoals) => {
    if (newSelectedGoals.length > 0) {
      getPatentStats(newSelectedGoals)
    } else {
      statsData.value = null
    }
  },
  { deep: true }, // Watch for changes in the array
)

let svg: d3.Selection<SVGSVGElement, unknown, HTMLElement, any>,
  g: d3.Selection<SVGGElement, unknown, HTMLElement, any>,
  path: d3.GeoPath<any, d3.GeoPermissibleObjects> | null = null,
  projection: d3.GeoProjection | null = null,
  zoom: d3.ZoomBehavior<Element, unknown>

const emit = defineEmits(['country-selected', 'update-selection'])
let currentTransform = d3.zoomIdentity
let countries: d3.Selection<SVGPathElement, d3.GeoPermissibleObjects, SVGGElement, unknown>

const updateTitleLanguage = () => {
  oddTitles = [
    t('sdg.1'),
    t('sdg.2'),
    t('sdg.3'),
    t('sdg.4'),
    t('sdg.5'),
    t('sdg.6'),
    t('sdg.7'),
    t('sdg.8'),
    t('sdg.9'),
    t('sdg.10'),
    t('sdg.11'),
    t('sdg.12'),
    t('sdg.13'),
    t('sdg.14'),
    t('sdg.15'),
    t('sdg.16'),
    t('sdg.17'),
  ]
}

const updateMapColors = () => {
  if (!countries) return

  const filteredSelectedGoals = selectedGoals.value.filter((goal) => goal !== 18)

  let singleGoal = null
  let multipleGoals: any[] = []

  if (filteredSelectedGoals.length === 1) {
    singleGoal = filteredSelectedGoals[0] // ID ODD
  } else if (filteredSelectedGoals.length > 1) {
    multipleGoals = filteredSelectedGoals // IDs ODD
  }

  countries
    .transition()
    .duration(500)
    .attr('fill', (d) => {
      const countryCode = (d as { id: number | undefined }).id
        ? ISONumtoISO3((d as { id: number | undefined }).id)
        : null

      if (!countryCode) return '#b7b7b7'

      let value = 0

      if (singleGoal) {
        const currentData = countryDataByOdd.value?.[singleGoal as number] || {}
        value = currentData[ISO3toISO2(countryCode)] || 0
        const maxValue = Math.max(...Object.values(currentData as Record<string, number>))
        const intensity = maxValue > 0 ? value / maxValue : 0
        const selectedOdd = odds.value.find((odd) => odd.id === singleGoal)
        selectedColor.value = selectedOdd ? selectedOdd.color : '#cccccc'
        return d3.interpolate('#b7b7b7', selectedColor.value)(intensity)
      } else if (multipleGoals.length > 1) {
        let totalValues: Record<string, any> = {}
        multipleGoals.forEach((goalId) => {
          const data = countryDataByOdd.value?.[goalId] || {}
          if (data && data[ISO3toISO2(countryCode)]) {
            value += data[ISO3toISO2(countryCode)]
          }
          for (const code in data) {
            totalValues[code] = (totalValues[code] || 0) + data[code]
          }
        })
        const maxValue = Math.max(...Object.values(totalValues))
        const intensity = maxValue > 0 ? value / maxValue : 0
        selectedColor.value = '#6F0474'
        return d3.interpolate('#b7b7b7', selectedColor.value)(intensity)
      } else {
        return '#b7b7b7'
      }
    })
}

const updateLegendTitle = () => {
  if (props.selectedGoals.length >= 2) {
    if (props.selectedGoals.length == 18) {
      selectedSdgTitle.value = t('explore.legendTitle.all')
    } else {
      selectedSdgTitle.value =
        props.selectedGoals.length + ' ' + t('explore.legendTitle.moreSelected')
    }
  } else if (props.selectedGoals.length == 1) {
    selectedSdgTitle.value = oddTitles[props.selectedGoals[0] as number]
  } else {
    selectedSdgTitle.value = t('explore.legendTitle.noSelected')
  }
}

const createMap = async () => {
  const mapElementWidth = document.getElementById('world-map')
  const width = mapElementWidth ? mapElementWidth.clientWidth : 0
  const mapElementHeight = document.getElementById('world-map')
  const height = mapElementHeight ? mapElementHeight.clientHeight : 0

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
      g.attr('transform', currentTransform.toString())

      g.selectAll('.country-label')
        .attr('font-size', () => {
          return `${8 / currentTransform.k > 3 ? 3 : 8 / currentTransform.k}px`
        })
        .style('visibility', currentTransform.k > 2 ? 'visible' : 'hidden')
    })

  svg.call(
    zoom as unknown as (selection: d3.Selection<SVGSVGElement, unknown, HTMLElement, any>) => void,
  )

  try {
    const worldData = (await d3.json(
      'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json',
    )) as Topology<Objects<GeoJsonProperties>>
    const geojson = feature(worldData, worldData.objects.countries)

    countries = g
      .selectAll<SVGPathElement, d3.GeoPermissibleObjects>('path')
      .data(
        'features' in geojson
          ? (geojson.features as d3.GeoPermissibleObjects[])
          : [geojson as d3.GeoPermissibleObjects],
      )
      .enter()
      .append('path')
      .attr('d', path as d3.ValueFn<SVGPathElement, unknown, string>)
      .attr('fill', '#f0f0f0')
      .attr('stroke', '#ccc')
      .attr('stroke-width', 0.5)
      .attr('data-code', (d) => ((d as { id: number | undefined }).id ?? '').toString())
      .on('mouseover', function () {
        d3.select(this).attr('stroke-width', 1.5).attr('stroke', '#ccc')
      })
      .on('mouseout', function () {
        d3.select(this).attr('stroke-width', 0.5).attr('stroke', '#ccc')
      })
      .on('click', (event, d) => {
        event.stopPropagation()
        if (!path) return
        const [[x0, y0], [x1, y1]] = path.bounds(d as d3.GeoPermissibleObjects)

        svg
          .transition()
          .duration(750)
          .call(
            zoom.transform as unknown as (
              transition: d3.Transition<SVGSVGElement, unknown, HTMLElement, any>,
              transform: d3.ZoomTransform,
            ) => void,
            d3.zoomIdentity
              .translate(width / 2, height / 2)
              .scale(Math.min(8, 0.9 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
              .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
          )
        countries
          .on('mouseover', function (event, d) {
            const countryCode = (d as { id: number | undefined }).id
              ? ISONumtoISO3((d as { id: number | undefined }).id)
              : null

            if (!countryCode) return

            const count = Object.values(countryDataByOdd.value).reduce(
              (acc, stats) => acc + (stats[ISO3toISO2(countryCode)] || 0),
              0,
            )

            const tooltip = document.getElementById('tooltip')
            if (tooltip) {
              tooltip.style.display = 'block'
              tooltip.innerHTML = `<strong>${countryCode}</strong>: ${count} patents`
            }
          })
          .on('mousemove', function (event) {
            const tooltip = document.getElementById('tooltip')
            if (tooltip) {
              const x = event.clientX || 0
              const y = event.clientY || 0

              tooltip.style.left = `${x + 20}px`
              tooltip.style.top = `${y + 20}px`
            }
          })
          .on('mouseout', function () {
            const tooltip = document.getElementById('tooltip')
            if (tooltip) {
              tooltip.style.display = 'none'
            }
          })
      })

    g.selectAll('text')
      .data('features' in geojson ? geojson.features : [])
      .enter()
      .append('text')
      .attr('class', 'country-label')
      .attr('x', (d) => (path ? path.centroid(d as d3.GeoPermissibleObjects)[0] : 0))
      .attr('y', (d) => (path ? path.centroid(d as d3.GeoPermissibleObjects)[1] : 0))
      .attr('text-anchor', 'middle')
      .attr('fill', '#333')
      .attr('font-size', '8px')
      .attr('font-weight', 'bold')
      .attr('pointer-events', 'none')

    svg.on('click', () => {
      return svg
        .transition()
        .duration(750)
        .call(
          zoom.transform as unknown as (
            transition: d3.Transition<SVGSVGElement, unknown, HTMLElement, any>,
            transform: d3.ZoomTransform,
          ) => void,
          d3.zoomIdentity,
        )
    })

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
          zoom.transform as unknown as (
            transition: d3.Transition<SVGSVGElement, unknown, HTMLElement, any>,
            transform: d3.ZoomTransform,
          ) => void,
          d3.zoomIdentity
            .translate(width / 2, height / 2)
            .scale(Math.min(8, 0.7 / Math.max((x1 - x0) / width, (y1 - y0) / height)))
            .translate(-(x0 + x1) / 2, -(y0 + y1) / 2),
        )
    }
  } catch (error) {
    console.error('Erreur lors du chargement des données de la carte:', error)
  }
}

watch(
  () => props.selectedGoals,
  () => {
    updateMapColors()
    updateLegendTitle()
    updateTitleLanguage()
  },
  { deep: true, immediate: true }, // optionnel, selon ton besoin
)

onMounted(() => {
  createMap()

  window.addEventListener('resize', () => {
    d3.select('#world-map svg').remove()
    createMap()
  })
})

const maxPatents = computed(() => {
  if (!statsData.value || !statsData.value.stats) return 0

  // Trouver le maximum de brevets pour un pays
  return Math.max(
    ...Object.values(statsData.value.stats).flatMap((countryStats) => Object.values(countryStats)),
  )
})
</script>

<template>
  <div class="map-and-sdg-container">
    <div class="map-container">
      <div id="world-map"></div>
      <div id="tooltip" class="tooltip" style="display: none"></div>
      <div class="legend">
        <div class="legend-title">
          {{ selectedSdgTitle }}
        </div>
        <div class="legend-scale" v-if="statsData">
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: '#b7b7b7' }"></div>
            <span>0</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor + '50' }"></div>
            <span>1-{{ Math.floor(maxPatents / 4) }}</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor + '70' }"></div>
            <span>{{ Math.floor(maxPatents / 4) + 1 }}-{{ Math.floor(maxPatents / 2) }}</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor + '99' }"></div>
            <span>{{ Math.floor(maxPatents / 2) + 1 }}-{{ Math.floor(maxPatents - 1) }}</span>
          </div>
          <div class="legend-item">
            <div class="legend-color" :style="{ backgroundColor: selectedColor }"></div>
            <span>{{ Math.floor(maxPatents) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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

.tooltip {
  position: fixed;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 5px 10px;
  font-size: 12px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  pointer-events: none;
  z-index: 10;
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
