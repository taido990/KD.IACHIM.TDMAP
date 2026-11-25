// Cổng Google Drive cho RKD_IACHIM.html (Google Apps Script) — TÙY CHỌN
// Trang đọc Drive trực tiếp bằng Drive API v3 + API Key; script này chỉ cần khi muốn LƯU GeoJSON chuyển đổi
// lên Drive (thư mục _geojson) để máy khác dùng chung (API Key không có quyền ghi).
// Triển khai: script.google.com › Dự án mới › dán file này › Deploy › New deployment › Web app
//   Execute as: Me · Who has access: Anyone → copy URL …/exec vào ô "URL Web App" trong trang WebGIS.
// Chỉ cho đọc/ghi trong các thư mục gốc khai báo ở ROOTS (và thư mục con của chúng).
const ROOTS = ['1J0KLgsIUw1qDbukXV2k5u6_qevNh3mKe'];   // RKD Ia Chim (Quảng Ngãi)
const CACHE_DIR = '_geojson';                            // nơi lưu GeoJSON chuyển đổi (cạnh bản vẽ)
const MAX_DEPTH = 4;                                     // số cấp thư mục con được quét

function doGet(e) {
  const p = e.parameter || {};
  try {
    if (p.action === 'list') return out_(list_(p.folder));
    if (p.action === 'get') return out_(get_(p.id, p.text === '1'));
    throw new Error('action không hợp lệ');
  } catch (err) { return out_({ error: String(err && err.message || err) }); }
}

function doPost(e) {
  try {
    const b = JSON.parse(e.postData.contents);
    if (b.action === 'save') return out_(save_(b));
    throw new Error('action không hợp lệ');
  } catch (err) { return out_({ error: String(err && err.message || err) }); }
}

function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

// File / thư mục có nằm trong một thư mục gốc được phép không (đi ngược lên các thư mục cha)
function inRoots_(item) {
  let q = [item]; const seen = {};
  for (let d = 0; d < 30 && q.length; d++) {
    const next = [];
    for (const x of q) {
      if (ROOTS.indexOf(x.getId()) >= 0) return true;
      const it = x.getParents();
      while (it.hasNext()) { const p = it.next(); if (!seen[p.getId()]) { seen[p.getId()] = 1; next.push(p); } }
    }
    q = next;
  }
  return false;
}

// Danh sách file (đệ quy, bỏ qua _geojson) + GeoJSON đệm (mô tả file lưu {src, stamp, crs, v})
function list_(folderId) {
  const root = DriveApp.getFolderById(folderId);
  if (!inRoots_(root)) throw new Error('thư mục không nằm trong ROOTS của drive_proxy.gs');
  const files = [];
  const walk = (f, path, depth) => {
    const it = f.getFiles();
    while (it.hasNext()) { const x = it.next(); files.push({ id: x.getId(), name: x.getName(), path: path + x.getName(), size: x.getSize(), modified: x.getLastUpdated().getTime() }); }
    if (depth >= MAX_DEPTH) return;
    const sub = f.getFolders();
    while (sub.hasNext()) { const s = sub.next(); if (s.getName() !== CACHE_DIR) walk(s, path + s.getName() + '/', depth + 1); }
  };
  walk(root, '', 0);
  const cache = {}, cd = root.getFoldersByName(CACHE_DIR);
  if (cd.hasNext()) {
    const it = cd.next().getFiles();
    while (it.hasNext()) {
      const x = it.next(); let d = null;
      try { d = JSON.parse(x.getDescription() || 'null'); } catch (_) { }
      if (d && d.src) cache[d.src] = { id: x.getId(), name: x.getName(), stamp: d.stamp, crs: d.crs, v: d.v, size: x.getSize() };
    }
  }
  return { folder: root.getName(), files: files, cache: cache };
}

function get_(id, asText) {
  const f = DriveApp.getFileById(id);
  if (!inRoots_(f)) throw new Error('file không nằm trong ROOTS của drive_proxy.gs');
  const b = f.getBlob();
  return asText ? { name: f.getName(), text: b.getDataAsString('UTF-8') } : { name: f.getName(), b64: Utilities.base64Encode(b.getBytes()) };
}

// Ghi / thay GeoJSON đệm của một bản vẽ vào <thư mục quét>/_geojson
function save_(b) {
  const root = DriveApp.getFolderById(b.folder);
  if (!inRoots_(root)) throw new Error('thư mục không nằm trong ROOTS của drive_proxy.gs');
  const src = DriveApp.getFileById(b.src);
  if (!inRoots_(src)) throw new Error('bản vẽ không nằm trong ROOTS của drive_proxy.gs');
  const cd = root.getFoldersByName(CACHE_DIR), dir = cd.hasNext() ? cd.next() : root.createFolder(CACHE_DIR);
  const lock = LockService.getScriptLock(); lock.waitLock(30000);
  try {
    const it = dir.getFiles();
    while (it.hasNext()) {
      const x = it.next(); let d = null;
      try { d = JSON.parse(x.getDescription() || 'null'); } catch (_) { }
      if (d && d.src === b.src) x.setTrashed(true);
    }
    const f = dir.createFile(Utilities.newBlob(b.text, 'application/geo+json', b.name));
    f.setDescription(JSON.stringify({ src: b.src, stamp: b.stamp, crs: b.crs, v: b.v }));
    return { ok: true, id: f.getId() };
  } finally { lock.releaseLock(); }
}
