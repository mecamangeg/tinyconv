// tinyconv web page: the same formula as tinyconv/units.py, base = value * factor + offset.
"use strict";

const $ = (id) => document.getElementById(id);
let UNITS = [];

function unitsIn(category) {
  return UNITS.filter((u) => u.category === category);
}

function fill(select, list, chosen) {
  select.replaceChildren(
    ...list.map((u) => new Option(`${u.name} (${u.symbol})`, u.symbol, false, u.symbol === chosen))
  );
}

function convert(value, a, b) {
  return (value * a.factor + a.offset - b.offset) / b.factor;
}

function show() {
  const value = parseFloat($("value").value);
  const a = UNITS.find((u) => u.symbol === $("src").value);
  const b = UNITS.find((u) => u.symbol === $("dst").value);
  if (!a || !b || Number.isNaN(value)) {
    $("result").textContent = "";
    return;
  }
  const r = convert(value, a, b);
  $("result").textContent = `${value} ${a.symbol} = ${Number(r.toPrecision(6))} ${b.symbol}`;
}

function pickCategory() {
  const list = unitsIn($("category").value);
  fill($("src"), list, list[0]?.symbol);
  fill($("dst"), list, list[1]?.symbol ?? list[0]?.symbol);
  show();
}

async function start() {
  try {
    const res = await fetch("units.json");
    if (!res.ok) throw new Error(`units.json: HTTP ${res.status}`);
    UNITS = (await res.json()).units;
  } catch (e) {
    $("error").textContent = `Couldn't load the unit table (${e.message}).`;
    $("error").hidden = false;
    return;
  }
  const cats = [...new Set(UNITS.map((u) => u.category))];
  $("category").replaceChildren(...cats.map((c) => new Option(c, c)));
  $("category").addEventListener("change", pickCategory);
  $("value").addEventListener("input", show);
  for (const id of ["src", "dst"]) $(id).addEventListener("change", show);
  $("swap").addEventListener("click", () => {
    const s = $("src").value;
    $("src").value = $("dst").value;
    $("dst").value = s;
    show();
  });
  pickCategory();
}

start();
