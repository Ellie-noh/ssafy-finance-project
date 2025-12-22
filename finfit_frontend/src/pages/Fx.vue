<template>
  <div class="fx">
    <header class="header">
      <h1 class="title">FX / Commodities</h1>
      <p class="subtitle">Spot price (dummy) · Minimal UI</p>
    </header>

    <!-- ✅ 자산 선택 + 기간 선택(기존) -->
    <section class="controls">
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: asset === 'gold' }"
          @click="asset = 'gold'"
          type="button"
        >
          Gold
        </button>
        <button
          class="tab"
          :class="{ active: asset === 'silver' }"
          @click="asset = 'silver'"
          type="button"
        >
          Silver
        </button>
      </div>

      <div class="ranges">
        <button
          v-for="r in ranges"
          :key="r.key"
          class="range"
          :class="{ active: rangeKey === r.key }"
          @click="rangeKey = r.key"
          type="button"
        >
          {{ r.label }}
        </button>
      </div>
    </section>

    <!-- ✅ (최소추가) 날짜 선택 UI + 잘못된 날짜 문구 -->
    <section class="dateBox">
      <div class="dateRow">
        <label class="dateLabel">
          <span>Start</span>
          <input class="dateInput" type="date" v-model="startDate" />
        </label>

        <label class="dateLabel">
          <span>End</span>
          <input class="dateInput" type="date" v-model="endDate" />
        </label>

        <button class="miniBtn" type="button" @click="clearDates">Clear</button>
      </div>

      <p v-if="dateError" class="dateError">{{ dateError }}</p>
      <p v-else class="dateHint">날짜를 선택하면 해당 기간만 표시합니다. (미선택 시 전체)</p>
    </section>

    <section class="summary">
      <div class="card">
        <div class="label">Latest</div>
        <div class="value">{{ formatPrice(summary.latest) }}</div>
        <div class="hint">{{ summary.latestDate }}</div>
      </div>

      <div class="card">
        <div class="label">Change</div>
        <div class="value" :class="{ up: summary.change >= 0, down: summary.change < 0 }">
          {{ formatSigned(summary.change) }}
          <span class="small">({{ formatSigned(summary.changePct) }}%)</span>
        </div>
        <div class="hint">vs first in range</div>
      </div>

      <div class="card">
        <div class="label">High / Low</div>
        <div class="value">
          {{ formatPrice(summary.high) }}
          <span class="small">/</span>
          {{ formatPrice(summary.low) }}
        </div>
        <div class="hint">within selected range</div>
      </div>

      <div class="card">
        <div class="label">Points</div>
        <div class="value">{{ filteredSeries.length }}</div>
        <div class="hint">data points</div>
      </div>
    </section>

    <section class="chartWrap">
      <div class="chartHeader">
        <div class="chartTitle">{{ assetLabel }} Spot Price</div>
        <div class="chartMeta">{{ rangeLabel }} · {{ filteredSeries.length }} pts</div>
      </div>

      <div class="chartCard">
        <svg
          class="chart"
          :viewBox="`0 0 ${width} ${height}`"
          @mousemove="onMove"
          @mouseleave="onLeave"
        >
          <path
            v-if="pathD"
            :d="pathD"
            fill="none"
            stroke="currentColor"
            stroke-width="2.2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <line
            v-if="hover.active"
            :x1="hover.x"
            y1="0"
            :x2="hover.x"
            :y2="height"
            stroke="#e5e7eb"
            stroke-width="1"
            stroke-dasharray="4 4"
          />

          <circle v-if="hover.active" :cx="hover.x" :cy="hover.y" r="4" fill="#111827" />
        </svg>

        <div v-if="hover.active" class="tooltip" :style="{ left: `${hover.clientX}px` }">
          <div class="ttDate">{{ hover.date }}</div>
          <div class="ttPrice">{{ formatPrice(hover.price) }}</div>
        </div>

        <div v-if="!pathD" class="empty">데이터가 없습니다.</div>
      </div>
    </section>

    <section class="note">
      <div class="noteTitle">Backend 연결할 때</div>
      <div class="noteText">아래 getFxData()만 axios로 바꾸면 화면 코드는 그대로 유지돼.</div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";

/**
 * ✅ 나중에 백엔드 붙일 때: 이 함수만 axios로 교체하면 됨.
 * 지금은 더미 데이터(금/은) 생성해서 반환.
 * 반환 형태: [{ date: 'YYYY-MM-DD', price: number }, ...]
 */
async function getFxData(assetKey) {
  const days = 365;
  const start = assetKey === "gold" ? 2000 : 25;
  const vol = assetKey === "gold" ? 18 : 0.45;

  const out = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let cur = start;

  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);

    const noise = (Math.random() - 0.5) * vol;
    cur = Math.max(0.01, cur + noise);

    out.push({
      date: toISODate(d),
      price: round2(cur),
    });
  }

  return out;
}

function toISODate(dateObj) {
  const y = dateObj.getFullYear();
  const m = String(dateObj.getMonth() + 1).padStart(2, "0");
  const d = String(dateObj.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function round2(n) {
  return Math.round(n * 100) / 100;
}

const asset = ref("gold");
const series = ref([]);

/** ✅ (최소추가) 날짜 범위 선택 */
const startDate = ref("");
const endDate = ref("");

const dateError = computed(() => {
  if (!startDate.value || !endDate.value) return "";
  if (startDate.value > endDate.value) return "시작일은 종료일보다 이전이어야 합니다.";
  return "";
});

function clearDates() {
  startDate.value = "";
  endDate.value = "";
}

const ranges = [
  { key: "1M", label: "1M", days: 30 },
  { key: "3M", label: "3M", days: 90 },
  { key: "6M", label: "6M", days: 180 },
  { key: "1Y", label: "1Y", days: 365 },
  { key: "ALL", label: "ALL", days: null },
];

const rangeKey = ref("3M");

const assetLabel = computed(() => (asset.value === "gold" ? "Gold" : "Silver"));
const rangeLabel = computed(() => ranges.find((r) => r.key === rangeKey.value)?.label ?? "ALL");

/**
 * ✅ 필터 우선순위
 * 1) 날짜가 둘 다 선택되어 있고, 오류가 없으면 날짜 필터
 * 2) 아니면 기존 rangeKey(1M/3M/...) 필터
 */
const filteredSeries = computed(() => {
  const data = series.value;

  // 날짜 필터
  if (startDate.value && endDate.value && !dateError.value) {
    return data.filter((d) => d.date >= startDate.value && d.date <= endDate.value);
  }

  // 기존 range 필터
  const r = ranges.find((x) => x.key === rangeKey.value);
  if (!r || !r.days) return data;

  const len = data.length;
  const startIndex = Math.max(0, len - r.days);
  return data.slice(startIndex);
});

const summary = computed(() => {
  const data = filteredSeries.value;
  if (!data.length) {
    return {
      latest: 0,
      latestDate: "-",
      first: 0,
      change: 0,
      changePct: 0,
      high: 0,
      low: 0,
    };
  }

  const first = data[0].price;
  const last = data[data.length - 1].price;

  let high = -Infinity;
  let low = Infinity;

  for (const p of data) {
    if (p.price > high) high = p.price;
    if (p.price < low) low = p.price;
  }

  const change = round2(last - first);
  const changePct = first === 0 ? 0 : round2((change / first) * 100);

  return {
    latest: last,
    latestDate: data[data.length - 1].date,
    first,
    change,
    changePct,
    high: round2(high),
    low: round2(low),
  };
});

/** ===== Chart (SVG) ===== */
const width = 900;
const height = 260;

const pathD = computed(() => {
  const data = filteredSeries.value;
  if (!data.length) return "";

  const prices = data.map((d) => d.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const span = Math.max(0.0001, max - min);

  const n = data.length;
  const xStep = n === 1 ? 0 : width / (n - 1);

  const points = data.map((d, i) => {
    const x = i * xStep;
    const y = height - ((d.price - min) / span) * height;
    return { x, y };
  });

  let d = `M ${points[0].x} ${points[0].y}`;
  for (let i = 1; i < points.length; i++) {
    d += ` L ${points[i].x} ${points[i].y}`;
  }
  return d;
});

const hover = reactive({
  active: false,
  x: 0,
  y: 0,
  price: 0,
  date: "",
  clientX: 0,
});

function onMove(e) {
  const data = filteredSeries.value;
  if (!data.length) return;

  const svg = e.currentTarget;
  const rect = svg.getBoundingClientRect();

  const px = e.clientX - rect.left;
  const ratio = Math.min(1, Math.max(0, px / rect.width));

  const idx = Math.round(ratio * (data.length - 1));
  const item = data[idx];

  const prices = data.map((d) => d.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const span = Math.max(0.0001, max - min);

  const x = (idx / Math.max(1, data.length - 1)) * width;
  const y = height - ((item.price - min) / span) * height;

  hover.active = true;
  hover.x = x;
  hover.y = y;
  hover.price = item.price;
  hover.date = item.date;
  hover.clientX = e.clientX;
}

function onLeave() {
  hover.active = false;
}

/** ===== Format ===== */
function formatPrice(n) {
  const unit = "USD/oz";
  return `${Number(n).toLocaleString()} ${unit}`;
}

function formatSigned(n) {
  const v = Number(n);
  if (v > 0) return `+${v}`;
  return `${v}`;
}

/** ===== Load ===== */
async function load() {
  series.value = await getFxData(asset.value);
}

onMounted(load);

watch(asset, async () => {
  await load();
  hover.active = false;
});
</script>

<style scoped>
.fx {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.header {
  padding: 6px 2px 0 2px;
}

.title {
  margin: 0;
  font-size: 22px;
  letter-spacing: -0.2px;
  color: #111827;
}

.subtitle {
  margin: 6px 0 0 0;
  color: #6b7280;
  font-size: 13px;
}

.controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.tabs {
  display: inline-flex;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
}

.tab {
  padding: 8px 12px;
  border: 0;
  background: transparent;
  cursor: pointer;
  font-weight: 700;
  color: #6b7280;
}

.tab.active {
  color: #111827;
  background: #f3f4f6;
}

.ranges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.range {
  padding: 8px 10px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: #fff;
  cursor: pointer;
  font-weight: 700;
  color: #374151;
  font-size: 13px;
}

.range.active {
  background: #111827;
  border-color: #111827;
  color: #fff;
}

/* ✅ (최소추가) 날짜 선택 UI */
.dateBox {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: #fff;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dateRow {
  display: flex;
  gap: 10px;
  align-items: end;
  flex-wrap: wrap;
}

.dateLabel {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
  font-weight: 800;
}

.dateInput {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px 12px;
  background: #fff;
  color: #111827;
  font-weight: 700;
}

.miniBtn {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px 12px;
  background: #fff;
  cursor: pointer;
  font-weight: 800;
  color: #111827;
}

.miniBtn:hover {
  background: #f9fafb;
}

.dateError {
  margin: 0;
  color: #991b1b;
  font-weight: 800;
  font-size: 12px;
}

.dateHint {
  margin: 0;
  color: #6b7280;
  font-weight: 800;
  font-size: 12px;
}

.summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.card {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 12px;
  background: #fff;
}

.label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 700;
}

.value {
  margin-top: 8px;
  font-size: 16px;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.2px;
}

.value.up {
  color: #065f46;
}

.value.down {
  color: #991b1b;
}

.small {
  font-size: 12px;
  font-weight: 800;
  margin-left: 6px;
  opacity: 0.85;
}

.hint {
  margin-top: 6px;
  font-size: 12px;
  color: #6b7280;
}

.chartWrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chartHeader {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.chartTitle {
  font-weight: 900;
  color: #111827;
}

.chartMeta {
  color: #6b7280;
  font-size: 12px;
  font-weight: 700;
}

.chartCard {
  position: relative;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: #fff;
  padding: 12px;
  overflow: hidden;
}

.chart {
  width: 100%;
  height: 260px;
  color: #111827;
}

.tooltip {
  position: fixed;
  top: 16px;
  transform: translateX(-50%);
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(6px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.06);
  pointer-events: none;
  z-index: 50;
  min-width: 140px;
}

.ttDate {
  font-size: 12px;
  color: #6b7280;
  font-weight: 800;
}

.ttPrice {
  margin-top: 6px;
  font-size: 14px;
  font-weight: 900;
  color: #111827;
}

.empty {
  padding: 24px;
  color: #6b7280;
  font-weight: 700;
}

.note {
  border: 1px dashed #e5e7eb;
  border-radius: 14px;
  padding: 12px;
  background: #fafafa;
}

.noteTitle {
  font-weight: 900;
  color: #111827;
  margin-bottom: 6px;
}

.noteText {
  color: #6b7280;
  font-size: 13px;
  font-weight: 700;
}

@media (max-width: 900px) {
  .summary {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
