<template>
  <section class="page">
    <h1 class="title">은행 찾기</h1>

    <div class="card">
      <select v-model="selectedProvince" class="select">
        <option value="">시/도 선택</option>
        <option v-for="province in provinces" :key="province" :value="province">{{ province }}</option>
      </select>
      <select v-model="selectedCity" class="select" :disabled="!selectedProvince">
        <option value="">시/군/구 선택</option>
        <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
      </select>
      <select v-model="selectedBank" class="select">
        <option value="">은행 선택</option>
        <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
      </select>
      <button @click="searchBanks" class="button" :disabled="!selectedProvince || !selectedCity || !selectedBank">찾기</button>

      <div class="list">
        <div v-for="place in places" :key="place.id" class="item">
          <div class="name">{{ place.place_name }}</div>
          <div class="addr">{{ place.address_name }}</div>
        </div>
      </div>
    </div>

    <div ref="mapContainer" style="width: 100%; height: 400px;" v-show="sdkLoaded"></div>
    <div v-if="!sdkLoaded">지도 로딩 중...</div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { API_KEY } from './apikey.js'
import data from './data.js'

const selectedProvince = ref('')
const selectedCity = ref('')
const selectedBank = ref('')
const places = ref([])
const sdkLoaded = ref(false)
const map = ref(null)
const markers = ref([])
const infowindow = ref(null)
const ps = ref(null)
const mapContainer = ref(null)

onMounted(() => {
  loadKakaoMapScript()
})

const loadKakaoMapScript = () => {
  if (window.kakao && window.kakao.maps) {
    kakao.maps.load(async () => {
      sdkLoaded.value = true
      await nextTick()
      initMap()
    })
    return
  }

  const script = document.createElement('script')
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false&libraries=services`
  script.onload = () => {
    kakao.maps.load(async () => {
      sdkLoaded.value = true
      await nextTick()
      initMap()
    })
  }
  script.onerror = () => {
    console.error('Kakao Maps SDK 로드 실패 - API 키를 확인하세요. developers.kakao.com에서 유효한 키를 발급받아 사용하세요.')
  }
  document.head.appendChild(script)
}

const initMap = () => {
  if (!mapContainer.value) {
    console.error('지도 컨테이너를 찾을 수 없습니다. DOM 로드 타이밍을 확인하세요.')
    return
  }
  const mapOption = {
    center: new kakao.maps.LatLng(37.498004, 127.027706),
    level: 3
  }

  map.value = new kakao.maps.Map(mapContainer.value, mapOption)
  ps.value = new kakao.maps.services.Places()
  infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 })
  console.log('Kakao Map 초기화 성공')
}

const provinces = computed(() => data.mapInfo.map(info => info.name))
const cities = computed(() => {
  if (!selectedProvince.value) return []
  const region = data.mapInfo.find(info => info.name === selectedProvince.value)
  return region ? region.countries : []
})
const banks = data.bankInfo

const searchBanks = () => {
  if (!sdkLoaded.value || !map.value || !ps.value) {
    alert('지도 또는 검색 서비스가 아직 로드되지 않았습니다. 잠시 후 다시 시도해주세요.')
    return
  }
  const keyword = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`
  console.log(`검색 시작: ${keyword}`)
  ps.value.keywordSearch(keyword, placesSearchCB, { useMapBounds: false })
}

const placesSearchCB = (data, status) => {
  if (status === kakao.maps.services.Status.OK) {
    places.value = data
    displayPlaces(data)
  } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 존재하지 않습니다.')
  } else if (status === kakao.maps.services.Status.ERROR) {
    alert('검색 중 오류가 발생했습니다. API 키가 유효한지 확인하세요.')
  }
}

const displayPlaces = (placesData) => {
  const bounds = new kakao.maps.LatLngBounds()

  removeMarkers()

  for (let i = 0; i < placesData.length; i++) {
    const place = placesData[i]
    const marker = new kakao.maps.Marker({
      map: map.value,
      position: new kakao.maps.LatLng(place.y, place.x)
    })

    markers.value.push(marker)

    kakao.maps.event.addListener(marker, 'click', () => {
      infowindow.value.setContent(`
        <div style="padding:5px;z-index:1; width:200px;">
          <strong>${place.place_name}</strong>
        </div>
      `)
      infowindow.value.open(map.value, marker)
    })

    bounds.extend(new kakao.maps.LatLng(place.y, place.x))
  }

  map.value.setBounds(bounds)
}

const removeMarkers = () => {
  for (let marker of markers.value) {
    marker.setMap(null)
  }
  markers.value = []
}
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.title {
  font-size: 24px;
  font-weight: 700;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  max-width: 520px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.select, .button {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px 12px;
  outline: none;
}

.button {
  background-color: #3b82f6;
  color: white;
  cursor: pointer;
}

.list {
  display: flex;
  flex-direction: column;
}

.item {
  padding: 10px 0;
  border-bottom: 1px solid #e5e7eb;
}

.item:last-child {
  border-bottom: none;
}

.name {
  font-weight: 600;
}

.addr {
  font-size: 13px;
  color: #6b7280;
}
</style>