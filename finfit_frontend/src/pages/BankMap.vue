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
    </div>

    <div ref="mapContainer" class="map-container" v-show="sdkLoaded"></div>
    <div v-if="!sdkLoaded">지도 로딩 중...</div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { API_KEY, REST_API_KEY } from './apikey.js'
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
    initMap()
    return
  }

  const script = document.createElement('script')
  script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}`
  script.onload = () => {
    nextTick(() => {
      initMap()
    })
  }
  script.onerror = (error) => {
    console.error('Kakao Maps SDK 로드 실패:', error)
    alert('지도 로드에 실패했습니다. 네트워크 연결을 확인해주세요.')
  }
  document.head.appendChild(script)
}

const initMap = () => {
  if (!mapContainer.value) {
    console.error('지도 컨테이너를 찾을 수 없습니다.')
    return
  }
  const mapOption = {
    center: new kakao.maps.LatLng(37.500486063, 127.022061548),
    level: 3
  }

  map.value = new kakao.maps.Map(mapContainer.value, mapOption)
  infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 })
  sdkLoaded.value = true

  // 지도 리사이즈 강제 호출
  setTimeout(() => {
    if (map.value) {
      map.value.relayout()
      console.log('지도 리사이즈 완료')
    }
  }, 100)

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
  if (!selectedProvince.value || !selectedCity.value || !selectedBank.value) {
    alert("모든 조건을 선택해주세요!")
    return
  }

  const keyword = `${selectedProvince.value} ${selectedCity.value} ${selectedBank.value}`
  console.log(`검색 시작: ${keyword}`)

  // Kakao 로컬 REST API 호출
  const url = `https://dapi.kakao.com/v2/local/search/keyword.json?query=${encodeURIComponent(keyword)}`

  fetch(url, {
    headers: {
      'Authorization': `KakaoAK ${REST_API_KEY}`
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.documents && data.documents.length > 0) {
      places.value = data.documents.map(place => ({
        place_name: place.place_name,
        address_name: place.address_name,
        y: place.y,
        x: place.x,
        id: place.id
      }))
      displayPlaces(places.value)
    } else {
      alert('검색 결과가 존재하지 않습니다.')
    }
  })
  .catch(error => {
    console.error('검색 오류:', error)
    alert('검색 중 오류가 발생했습니다.')
  })
}

const displayPlaces = (placesData) => {
  removeMarkers()

  if (placesData.length === 0) return

  const bounds = new kakao.maps.LatLngBounds()

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
          <strong>${place.place_name}</strong><br>
          ${place.address_name}
        </div>
      `)
      infowindow.value.open(map.value, marker)
    })

    bounds.extend(new kakao.maps.LatLng(place.y, place.x))
  }

  // 검색 결과가 있으면 bounds 설정, 없으면 기본 위치 유지
  if (placesData.length > 0) {
    map.value.setBounds(bounds)
  }
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

.map-container {
  width: 100%;
  height: 500px;
  min-height: 400px;
  position: relative;
  border-radius: 12px;
  overflow: hidden;
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