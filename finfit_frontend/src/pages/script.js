let map;                // 지도 객체
let ps;                 // 장소 검색 객체 (Python의 라이브러리 인스턴스 같은 것)
let infowindow;         // 마커 클릭 시 뜨는 말풍선
let markers = [];       // 지도에 찍힌 마커들을 담아둘 리스트 (지우기 위해 필요)

// =================
// 초기화 및 지도 로드
// =================
function loadKakaoMapScript() {
    const script = document.createElement('script');
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false&libraries=services`;
    document.head.appendChild(script);
    script.onload = () => {
        kakao.maps.load(() => {
            initMap();
        });
    };
}

function initMap() {
    const mapContainer = document.getElementById('map');
    const mapOption = {
        center: new kakao.maps.LatLng(37.498004, 127.027706),
        level: 3
    };

    map = new kakao.maps.Map(mapContainer, mapOption);

    ps = new kakao.maps.services.Places();

    infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });

    console.log("지도와 검색 서비스 로드 완료!");
}

// 프로그램 시작
loadKakaoMapScript();


// ==============
// UI 및 검색 로직
// ==============
const provinceSelect = document.getElementById('province');
const citySelect = document.getElementById('city');
const bankSelect = document.getElementById('bank');
const searchBtn = document.getElementById('searchBtn');

// 드롭다운 초기화
data.mapInfo.forEach(info => {
    const option = document.createElement('option');
    option.value = info.name;
    option.innerText = info.name;
    provinceSelect.appendChild(option);
});

data.bankInfo.forEach(bankName => {
    const option = document.createElement('option');
    option.value = bankName;
    option.innerText = bankName;
    bankSelect.appendChild(option);
});

provinceSelect.addEventListener('change', (event) => {
    const selectedProvince = event.target.value;
    citySelect.innerHTML = '<option value="">시/군/구 선택</option>';
    if (!selectedProvince) return;

    const foundRegion = data.mapInfo.find(info => info.name === selectedProvince);
    if (foundRegion) {
        foundRegion.countries.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.innerText = city;
            citySelect.appendChild(option);
        });
    }
});


// 찾기 버튼 클릭 시
searchBtn.addEventListener('click', () => {
    const province = provinceSelect.value;
    const city = citySelect.value;
    const bank = bankSelect.value;

    if (!province || !city || !bank) {
        alert("모든 조건을 선택해주세요!");
        return;
    }

    // 검색어 조합 (예: "서울특별시 강남구 국민은행")
    const keyword = `${province} ${city} ${bank}`;
    console.log(`검색 시작: ${keyword}`);

    // 카카오 장소 검색 API 호출
    // keywordSearch(검색어, 콜백함수)
    ps.keywordSearch(keyword, placesSearchCB);
});


// 검색 결과 처리 콜백 함수
// data: 검색 결과 리스트, status: 성공여부
function placesSearchCB(data, status, pagination) {
    if (status === kakao.maps.services.Status.OK) {
        
        displayPlaces(data);

    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
        alert('검색 결과가 존재하지 않습니다.');
        return;
    } else if (status === kakao.maps.services.Status.ERROR) {
        alert('검색 중 오류가 발생했습니다.');
        return;
    }
}

// 마커 표시 및 지도 범위 재설정 함수
function displayPlaces(places) {
    const listEl = document.getElementById('placesList');
    const bounds = new kakao.maps.LatLngBounds(); // 지도의 범위를 재설정하기 위한 객체

    // 기존에 찍혀있던 마커 제거 (초기화)
    removeMarker();

    for (let i = 0; i < places.length; i++) {
        // 마커를 생성하고 지도에 표시
        addMarker(places[i]);

        // 검색된 장소 위치를 기준으로 지도 범위(Bounds)를 확장
        bounds.extend(new kakao.maps.LatLng(places[i].y, places[i].x));
    }

    // 검색된 장소들이 모두 보이도록 지도 범위 재설정
    map.setBounds(bounds);
}

// 마커 생성 함수
function addMarker(place) {
    const marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(place.y, place.x) 
    });

    // 마커 배열에 저장 (나중에 지우기 위함)
    markers.push(marker);

    // 마커 클릭 이벤트: 인포윈도우(말풍선) 띄우기
    kakao.maps.event.addListener(marker, 'click', function() {
        const content = `
            <div style="padding:5px;z-index:1; width:200px;">
                <strong>${place.place_name}</strong>
            </div>
        `;
        
        infowindow.setContent(content);
        infowindow.open(map, marker);
    });
}

// 마커 제거 함수
function removeMarker() {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(null); 
    }
    markers = [];
}
