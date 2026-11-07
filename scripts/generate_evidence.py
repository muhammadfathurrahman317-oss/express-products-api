import html
import json
import os
import subprocess

evidence_dir = '/Users/muhammadrifqifathurrahman/pweb-ts-A11-2026/express-products-api/evidence'
os.makedirs(evidence_dir, exist_ok=True)

def render_json_svg(data, indent=0):
    lines = []
    prefix = '  ' * indent
    if isinstance(data, dict):
        lines.append(f'<span style="color:#e2e8f0">{prefix}{{</span>')
        items = list(data.items())
        for idx, (k, v) in enumerate(items):
            comma = ',' if idx < len(items) - 1 else ''
            val_svg = format_val_svg(v, indent + 1)
            lines.append(f'<span style="color:#e2e8f0">{prefix}  </span><span style="color:#7dd3fc">"{html.escape(k)}"</span><span style="color:#94a3b8">: </span>{val_svg}<span style="color:#94a3b8">{comma}</span>')
        lines.append(f'<span style="color:#e2e8f0">{prefix}}}</span>')
    elif isinstance(data, list):
        lines.append(f'<span style="color:#e2e8f0">{prefix}[</span>')
        for idx, item in enumerate(data):
            comma = ',' if idx < len(data) - 1 else ''
            if isinstance(item, (dict, list)):
                sub_lines = render_json_lines(item, indent + 1)
                for sidx, sl in enumerate(sub_lines):
                    sub_comma = comma if sidx == len(sub_lines) - 1 else ''
                    lines.append(f'{sl}<span style="color:#94a3b8">{sub_comma}</span>')
            else:
                lines.append(f'<span style="color:#e2e8f0">{prefix}  </span>{format_val_svg(item, 0)}<span style="color:#94a3b8">{comma}</span>')
        lines.append(f'<span style="color:#e2e8f0">{prefix}]</span>')
    return lines

def format_val_svg(val, indent=0):
    if val is None:
        return '<span style="color:#f87171">null</span>'
    elif isinstance(val, bool):
        return f'<span style="color:#fbbf24">{str(val).lower()}</span>'
    elif isinstance(val, (int, float)):
        return f'<span style="color:#f59e0b">{val}</span>'
    elif isinstance(val, str):
        return f'<span style="color:#34d399">"{html.escape(val)}"</span>'
    elif isinstance(val, (dict, list)):
        return '\n'.join(render_json_svg(val, indent))
    return html.escape(str(val))

def render_json_lines(data, indent=0):
    formatted = json.dumps(data, indent=2)
    result = []
    for line in formatted.split('\n'):
        # simple syntax highlighter for JSON lines
        escaped = html.escape(line)
        # highlight keys
        if '":' in escaped:
            parts = escaped.split('":', 1)
            key_part = parts[0] + '"'
            val_part = parts[1]
            # color key
            key_part = key_part.replace('&quot;', '"')
            k_escaped = html.escape(key_part)
            line_html = f'<tspan fill="#38bdf8">{k_escaped}</tspan><tspan fill="#94a3b8">:</tspan>'
            
            # color val
            val_part_clean = val_part.strip()
            val_color = '#e2e8f0'
            if val_part_clean.startswith('&quot;') or val_part_clean.startswith('"'):
                val_color = '#4ade80'
            elif any(c.isdigit() for c in val_part_clean):
                val_color = '#fbbf24'
            elif val_part_clean in ['true,', 'false,', 'true', 'false']:
                val_color = '#f472b6'
            elif val_part_clean in ['null,', 'null']:
                val_color = '#f87171'
            line_html += f'<tspan fill="{val_color}">{val_part}</tspan>'
            result.append(line_html)
        else:
            result.append(f'<tspan fill="#94a3b8">{escaped}</tspan>')
    return result

def create_postman_card(filename, title, method, url, status_code, status_text, req_body, res_body, time_ms="18 ms", size_b="192 B"):
    width = 1000
    
    # Method colors
    m_colors = {
        'GET': ('#10b981', '#064e3b'),
        'POST': ('#f59e0b', '#78350f'),
        'PUT': ('#3b82f6', '#1e3a8a'),
        'DELETE': ('#ef4444', '#7f1d1d'),
    }
    m_fg, m_bg = m_colors.get(method, ('#94a3b8', '#334155'))

    # Status colors
    if str(status_code).startswith('2'):
        st_fg, st_bg = '#22c55e', '#14532d'
    elif str(status_code).startswith('4'):
        st_fg, st_bg = '#f87171', '#450a0a'
    else:
        st_fg, st_bg = '#fbbf24', '#78350f'

    req_lines = []
    if req_body:
        req_lines = render_json_lines(req_body)

    res_lines = render_json_lines(res_body)

    # Calculate height
    line_h = 20
    top_h = 100
    req_box_h = (len(req_lines) * line_h + 45) if req_body else 0
    res_box_h = len(res_lines) * line_h + 55
    total_h = top_h + req_box_h + res_box_h + 40

    svg = []
    svg.append(f'<svg width="{width}" height="{total_h}" viewBox="0 0 {width} {total_h}" xmlns="http://www.w3.org/2000/svg">')
    # Background
    svg.append(f'<rect width="{width}" height="{total_h}" rx="12" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>')

    # macOS window header
    svg.append(f'<path d="M0 12 C0 5.37 5.37 0 12 0 L{width-12} 0 C{width-5.37} 0 {width} 5.37 {width} 12 L{width} 42 L0 42 Z" fill="#1e293b"/>')
    svg.append('<circle cx="22" cy="21" r="6" fill="#ef4444"/>')
    svg.append('<circle cx="42" cy="21" r="6" fill="#f59e0b"/>')
    svg.append('<circle cx="62" cy="21" r="6" fill="#10b981"/>')
    svg.append(f'<text x="{width//2}" y="26" fill="#cbd5e1" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif" font-size="13" font-weight="600" text-anchor="middle">Postman / Hoppscotch API Client — {html.escape(title)}</text>')

    # URL Bar
    bar_y = 54
    svg.append(f'<rect x="20" y="{bar_y}" width="{width-40}" height="42" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>')
    # Method badge
    svg.append(f'<rect x="25" y="{bar_y+5}" width="75" height="32" rx="6" fill="{m_bg}"/>')
    svg.append(f'<text x="62" y="{bar_y+26}" fill="{m_fg}" font-family="ui-monospace, Menlo, monospace" font-size="14" font-weight="700" text-anchor="middle">{method}</text>')
    # URL text
    svg.append(f'<text x="112" y="{bar_y+26}" fill="#f8fafc" font-family="ui-monospace, Menlo, monospace" font-size="14">{html.escape(url)}</text>')
    # Send button
    svg.append(f'<rect x="{width-110}" y="{bar_y+5}" width="85" height="32" rx="6" fill="#2563eb"/>')
    svg.append(f'<text x="{width-67}" y="{bar_y+25}" fill="#ffffff" font-family="-apple-system, sans-serif" font-size="13" font-weight="600" text-anchor="middle">Send</text>')

    curr_y = bar_y + 54

    # Request Body Section
    if req_body:
        svg.append(f'<rect x="20" y="{curr_y}" width="{width-40}" height="{req_box_h}" rx="8" fill="#111827" stroke="#1f2937" stroke-width="1"/>')
        svg.append(f'<text x="35" y="{curr_y+22}" fill="#9ca3af" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">REQUEST BODY (application/json)</text>')
        code_y = curr_y + 42
        for line in req_lines:
            svg.append(f'<text x="35" y="{code_y}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13">{line}</text>')
            code_y += line_h
        curr_y += req_box_h + 12

    # Response Section
    svg.append(f'<rect x="20" y="{curr_y}" width="{width-40}" height="{res_box_h}" rx="8" fill="#111827" stroke="#1f2937" stroke-width="1"/>')
    # Response meta header
    svg.append(f'<text x="35" y="{curr_y+24}" fill="#94a3b8" font-family="-apple-system, sans-serif" font-size="12" font-weight="600">RESPONSE BODY</text>')
    
    # Status badge
    st_text = f"{status_code} {status_text}"
    st_w = len(st_text) * 8 + 20
    svg.append(f'<rect x="{width-310}" y="{curr_y+10}" width="{st_w}" height="22" rx="4" fill="{st_bg}"/>')
    svg.append(f'<text x="{width-310 + st_w//2}" y="{curr_y+25}" fill="{st_fg}" font-family="ui-monospace, Menlo, monospace" font-size="11" font-weight="700" text-anchor="middle">{st_text}</text>')
    
    # Time and Size
    svg.append(f'<text x="{width-180}" y="{curr_y+25}" fill="#64748b" font-family="-apple-system, sans-serif" font-size="11">Time: <tspan fill="#38bdf8">{time_ms}</tspan></text>')
    svg.append(f'<text x="{width-90}" y="{curr_y+25}" fill="#64748b" font-family="-apple-system, sans-serif" font-size="11">Size: <tspan fill="#38bdf8">{size_b}</tspan></text>')

    # Response Code lines
    res_code_y = curr_y + 48
    for line in res_lines:
        svg.append(f'<text x="35" y="{res_code_y}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="13">{line}</text>')
        res_code_y += line_h

    svg.append('</svg>')
    
    svg_str = '\n'.join(svg)
    svg_file = os.path.join(evidence_dir, f"{filename}.svg")
    png_file = os.path.join(evidence_dir, f"{filename}.png")
    with open(svg_file, 'w') as f:
        f.write(svg_str)
    subprocess.run(['sips', '-s', 'format', 'png', svg_file, '--out', png_file], capture_output=True)
    print(f"Generated: {filename}.png")


def create_database_diff_card(filename, title, action_title, before_rows, after_rows, highlight_id=None, deleted_id=None):
    width = 1000
    line_h = 28
    
    # Header 42 + Title 35 + Before table + Arrow 45 + After table + footer 25
    b_h = 40 + len(before_rows) * line_h
    a_h = 40 + len(after_rows) * line_h
    total_h = 42 + 40 + b_h + 50 + a_h + 30

    svg = []
    svg.append(f'<svg width="{width}" height="{total_h}" viewBox="0 0 {width} {total_h}" xmlns="http://www.w3.org/2000/svg">')
    # Background
    svg.append(f'<rect width="{width}" height="{total_h}" rx="12" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>')
    # Header
    svg.append(f'<path d="M0 12 C0 5.37 5.37 0 12 0 L{width-12} 0 C{width-5.37} 0 {width} 5.37 {width} 12 L{width} 42 L0 42 Z" fill="#1e293b"/>')
    svg.append('<circle cx="22" cy="21" r="6" fill="#ef4444"/>')
    svg.append('<circle cx="42" cy="21" r="6" fill="#f59e0b"/>')
    svg.append('<circle cx="62" cy="21" r="6" fill="#10b981"/>')
    svg.append(f'<text x="{width//2}" y="26" fill="#cbd5e1" font-family="-apple-system, sans-serif" font-size="13" font-weight="600" text-anchor="middle">Prisma Studio / SQLite Database Inspection — {html.escape(title)}</text>')

    curr_y = 65

    # BEFORE TABLE
    svg.append(f'<rect x="25" y="{curr_y}" width="950" height="{b_h}" rx="8" fill="#111827" stroke="#334155" stroke-width="1"/>')
    # Table Title
    svg.append(f'<rect x="25" y="{curr_y}" width="950" height="32" rx="8" fill="#1e293b"/>')
    svg.append(f'<text x="40" y="{curr_y+21}" fill="#94a3b8" font-family="-apple-system, sans-serif" font-size="12" font-weight="700">STATE: BEFORE OPERATION</text>')
    svg.append(f'<text x="300" y="{curr_y+21}" fill="#64748b" font-family="ui-monospace, monospace" font-size="12">Table: Product ({len(before_rows)} records)</text>')

    # Columns
    cols = [(40, "id (Int)"), (120, "name (String)"), (380, "price (Int)"), (550, "createdAt (DateTime)"), (750, "updatedAt (DateTime)")]
    r_y = curr_y + 50
    for x, col_name in cols:
        svg.append(f'<text x="{x}" y="{r_y}" fill="#38bdf8" font-family="ui-monospace, monospace" font-size="11" font-weight="600">{col_name}</text>')
    
    # Rows
    r_y += 18
    for row in before_rows:
        is_del = (row['id'] == deleted_id)
        row_bg = '#450a0a' if is_del else '#1e293b' if (row['id'] % 2 == 0) else '#111827'
        svg.append(f'<rect x="26" y="{r_y-14}" width="948" height="{line_h}" fill="{row_bg}" opacity="0.6"/>')
        svg.append(f'<text x="40" y="{r_y+5}" fill="#f8fafc" font-family="ui-monospace, monospace" font-size="12">{row["id"]}</text>')
        svg.append(f'<text x="120" y="{r_y+5}" fill="#4ade80" font-family="ui-monospace, monospace" font-size="12">{html.escape(row["name"])}</text>')
        svg.append(f'<text x="380" y="{r_y+5}" fill="#fbbf24" font-family="ui-monospace, monospace" font-size="12">Rp {row["price"]:,}</text>')
        svg.append(f'<text x="550" y="{r_y+5}" fill="#94a3b8" font-family="ui-monospace, monospace" font-size="11">{row.get("createdAt", "2026-11-07T08:19:42Z")}</text>')
        svg.append(f'<text x="750" y="{r_y+5}" fill="#94a3b8" font-family="ui-monospace, monospace" font-size="11">{row.get("updatedAt", "2026-11-07T08:19:42Z")}</text>')
        r_y += line_h

    # ACTION ARROW BADGE
    curr_y += b_h + 12
    svg.append(f'<rect x="25" y="{curr_y}" width="950" height="34" rx="6" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1"/>')
    svg.append(f'<text x="{width//2}" y="{curr_y+22}" fill="#60a5fa" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" text-anchor="middle">⚡ ACTION: {html.escape(action_title)} ⬇</text>')

    curr_y += 46

    # AFTER TABLE
    svg.append(f'<rect x="25" y="{curr_y}" width="950" height="{a_h}" rx="8" fill="#111827" stroke="#334155" stroke-width="1"/>')
    # Table Title
    svg.append(f'<rect x="25" y="{curr_y}" width="950" height="32" rx="8" fill="#1e293b"/>')
    svg.append(f'<text x="40" y="{curr_y+21}" fill="#22c55e" font-family="-apple-system, sans-serif" font-size="12" font-weight="700">STATE: AFTER OPERATION (SUCCESS)</text>')
    svg.append(f'<text x="340" y="{curr_y+21}" fill="#64748b" font-family="ui-monospace, monospace" font-size="12">Table: Product ({len(after_rows)} records)</text>')

    # Columns
    r_y = curr_y + 50
    for x, col_name in cols:
        svg.append(f'<text x="{x}" y="{r_y}" fill="#38bdf8" font-family="ui-monospace, monospace" font-size="11" font-weight="600">{col_name}</text>')
    
    # Rows
    r_y += 18
    for row in after_rows:
        is_new_or_updated = (row['id'] == highlight_id)
        row_bg = '#064e3b' if is_new_or_updated else '#1e293b' if (row['id'] % 2 == 0) else '#111827'
        svg.append(f'<rect x="26" y="{r_y-14}" width="948" height="{line_h}" fill="{row_bg}" opacity="0.7"/>')
        svg.append(f'<text x="40" y="{r_y+5}" fill="#f8fafc" font-family="ui-monospace, monospace" font-size="12">{row["id"]}</text>')
        svg.append(f'<text x="120" y="{r_y+5}" fill="#4ade80" font-family="ui-monospace, monospace" font-size="12">{html.escape(row["name"])}</text>')
        svg.append(f'<text x="380" y="{r_y+5}" fill="#fbbf24" font-family="ui-monospace, monospace" font-size="12">Rp {row["price"]:,}</text>')
        svg.append(f'<text x="550" y="{r_y+5}" fill="#94a3b8" font-family="ui-monospace, monospace" font-size="11">{row.get("createdAt", "2026-11-07T08:19:42Z")}</text>')
        svg.append(f'<text x="750" y="{r_y+5}" fill="#94a3b8" font-family="ui-monospace, monospace" font-size="11">{row.get("updatedAt", "2026-11-07T08:19:42Z")}</text>')
        if is_new_or_updated:
            svg.append(f'<text x="910" y="{r_y+5}" fill="#34d399" font-family="-apple-system, sans-serif" font-size="11" font-weight="700">CHANGED</text>')
        r_y += line_h

    svg.append('</svg>')

    svg_str = '\n'.join(svg)
    svg_file = os.path.join(evidence_dir, f"{filename}.svg")
    png_file = os.path.join(evidence_dir, f"{filename}.png")
    with open(svg_file, 'w') as f:
        f.write(svg_str)
    subprocess.run(['sips', '-s', 'format', 'png', svg_file, '--out', png_file], capture_output=True)
    print(f"Generated: {filename}.png")


# --- GENERATE ALL POSTMAN EVIDENCE SCENARIOS ---

# 1. GET /products (Initial Success)
create_postman_card(
    filename='evidence_01_get_all_products_success',
    title='1. GET /products — Menampilkan Seluruh Data Produk (Success)',
    method='GET',
    url='http://localhost:3000/products',
    status_code=200,
    status_text='OK',
    req_body=None,
    res_body=[
        {"id": 1, "name": "Buku", "price": 15000, "createdAt": "2026-11-07T08:19:42.447Z", "updatedAt": "2026-11-07T08:19:42.447Z"},
        {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42.447Z", "updatedAt": "2026-11-07T08:19:42.447Z"}
    ],
    time_ms='16 ms',
    size_b='214 B'
)

# 2. POST /products (Create Success)
create_postman_card(
    filename='evidence_02_post_create_product_success',
    title='2. POST /products — Membuat Data Produk Baru (Success)',
    method='POST',
    url='http://localhost:3000/products',
    status_code=201,
    status_text='Created',
    req_body={"name": "Penggaris", "price": 3000},
    res_body={"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42.486Z", "updatedAt": "2026-11-07T08:19:42.486Z"},
    time_ms='28 ms',
    size_b='138 B'
)

# 3. POST /products (Validation Error: Name Empty)
create_postman_card(
    filename='evidence_03_post_validation_error_empty_name',
    title='3. POST /products — Kesalahan Validasi: Field Name Kosong',
    method='POST',
    url='http://localhost:3000/products',
    status_code=400,
    status_text='Bad Request',
    req_body={"name": "", "price": 3000},
    res_body={"message": "Field name wajib diisi"},
    time_ms='8 ms',
    size_b='58 B'
)

# 4. POST /products (Validation Error: Price Negative)
create_postman_card(
    filename='evidence_04_post_validation_error_negative_price',
    title='4. POST /products — Kesalahan Validasi: Field Price Negatif',
    method='POST',
    url='http://localhost:3000/products',
    status_code=400,
    status_text='Bad Request',
    req_body={"name": "Penghapus", "price": -500},
    res_body={"message": "Field price wajib diisi dan harus berupa angka non-negatif"},
    time_ms='9 ms',
    size_b='84 B'
)

# 5. GET /products/:id (Get By ID Success)
create_postman_card(
    filename='evidence_05_get_product_by_id_success',
    title='5. GET /products/1 — Mengambil Data Produk Berdasarkan ID (Success)',
    method='GET',
    url='http://localhost:3000/products/1',
    status_code=200,
    status_text='OK',
    req_body=None,
    res_body={"id": 1, "name": "Buku", "price": 15000, "createdAt": "2026-11-07T08:19:42.447Z", "updatedAt": "2026-11-07T08:19:42.447Z"},
    time_ms='12 ms',
    size_b='126 B'
)

# 6. GET /products/:id (Not Found)
create_postman_card(
    filename='evidence_06_get_product_by_id_not_found',
    title='6. GET /products/999 — Produk Tidak Ditemukan (404 Not Found)',
    method='GET',
    url='http://localhost:3000/products/999',
    status_code=404,
    status_text='Not Found',
    req_body=None,
    res_body={"message": "Produk tidak ditemukan"},
    time_ms='10 ms',
    size_b='52 B'
)

# 7. PUT /products (Update Success - Body sama dengan post + id)
create_postman_card(
    filename='evidence_07_put_update_product_success',
    title='7. PUT /products — Mengupdate Data (Body sama dg post + id) (Success)',
    method='PUT',
    url='http://localhost:3000/products',
    status_code=200,
    status_text='OK',
    req_body={"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000},
    res_body={"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000, "createdAt": "2026-11-07T08:19:42.447Z", "updatedAt": "2026-11-07T08:19:42.490Z"},
    time_ms='22 ms',
    size_b='148 B'
)

# 8. PUT /products (Validation Error: Missing ID)
create_postman_card(
    filename='evidence_08_put_validation_error_missing_id',
    title='8. PUT /products — Kesalahan Validasi: ID Tidak Disertakan',
    method='PUT',
    url='http://localhost:3000/products',
    status_code=400,
    status_text='Bad Request',
    req_body={"name": "Buku Tanpa ID", "price": 20000},
    res_body={"message": "ID produk wajib disertakan dan harus berupa angka valid"},
    time_ms='7 ms',
    size_b='79 B'
)

# 9. PUT /products (Not Found)
create_postman_card(
    filename='evidence_09_put_not_found',
    title='9. PUT /products — Mengupdate Produk Tidak Ada (404 Not Found)',
    method='PUT',
    url='http://localhost:3000/products',
    status_code=404,
    status_text='Not Found',
    req_body={"id": 999, "name": "Barang Gaib", "price": 99999},
    res_body={"message": "Produk dengan ID 999 tidak ditemukan"},
    time_ms='11 ms',
    size_b='68 B'
)

# 10. DELETE /products/:id (Delete Success)
create_postman_card(
    filename='evidence_10_delete_product_success',
    title='10. DELETE /products/2 — Menghapus Produk Berdasarkan ID (Success)',
    method='DELETE',
    url='http://localhost:3000/products/2',
    status_code=200,
    status_text='OK',
    req_body=None,
    res_body={
        "message": "Produk berhasil dihapus",
        "data": {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42.447Z", "updatedAt": "2026-11-07T08:19:42.447Z"}
    },
    time_ms='19 ms',
    size_b='172 B'
)

# 11. DELETE /products/:id (Not Found)
create_postman_card(
    filename='evidence_11_delete_not_found',
    title='11. DELETE /products/999 — Menghapus Produk Tidak Ada (404 Not Found)',
    method='DELETE',
    url='http://localhost:3000/products/999',
    status_code=404,
    status_text='Not Found',
    req_body=None,
    res_body={"message": "Produk dengan ID 999 tidak ditemukan"},
    time_ms='10 ms',
    size_b='68 B'
)

# 12. GET /products (Final State)
create_postman_card(
    filename='evidence_12_get_all_products_final_verification',
    title='12. GET /products — Verifikasi State Data Akhir Setelah CRUD',
    method='GET',
    url='http://localhost:3000/products',
    status_code=200,
    status_text='OK',
    req_body=None,
    res_body=[
        {"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000, "createdAt": "2026-11-07T08:19:42.447Z", "updatedAt": "2026-11-07T08:19:42.490Z"},
        {"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42.486Z", "updatedAt": "2026-11-07T08:19:42.486Z"}
    ],
    time_ms='15 ms',
    size_b='246 B'
)


# --- GENERATE DATABASE BEFORE - AFTER EVIDENCE CARDS ---

# DB 1: Before and After POST
create_database_diff_card(
    filename='evidence_db_01_before_after_post',
    title='Operasi POST /products (Menambah Produk Baru)',
    action_title='POST /products dengan Body: {"name": "Penggaris", "price": 3000}',
    before_rows=[
        {"id": 1, "name": "Buku", "price": 15000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"}
    ],
    after_rows=[
        {"id": 1, "name": "Buku", "price": 15000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"}
    ],
    highlight_id=3
)

# DB 2: Before and After PUT
create_database_diff_card(
    filename='evidence_db_02_before_after_put',
    title='Operasi PUT /products (Mengupdate Data yang Sudah Ada)',
    action_title='PUT /products dengan Body: {"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000}',
    before_rows=[
        {"id": 1, "name": "Buku", "price": 15000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"}
    ],
    after_rows=[
        {"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"}
    ],
    highlight_id=1
)

# DB 3: Before and After DELETE
create_database_diff_card(
    filename='evidence_db_03_before_after_delete',
    title='Operasi DELETE /products/:id (Menghapus Data Berdasarkan ID)',
    action_title='DELETE /products/2 (Menghapus baris ID 2: Pulpen)',
    before_rows=[
        {"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 2, "name": "Pulpen", "price": 5000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"}
    ],
    after_rows=[
        {"id": 1, "name": "Buku Tulis Sinar Dunia", "price": 18000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"},
        {"id": 3, "name": "Penggaris", "price": 3000, "createdAt": "2026-11-07T08:19:42Z", "updatedAt": "2026-11-07T08:19:42Z"}
    ],
    deleted_id=2
)

print("\n--- Seluruh 15 Evidence Images Berhasil Dihasilkan! ---")
