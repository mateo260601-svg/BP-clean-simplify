<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BP Generator — MG</title>
<link rel="icon" type="image/png" href="/assets/icon_32.png">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f0f2f5;color:#111;-webkit-font-smoothing:antialiased}
button{cursor:pointer;font-family:inherit}
button:disabled{opacity:.38;cursor:not-allowed}
input{font-family:inherit}

#app{min-height:100vh}
.screen{display:none}
.screen.active{display:flex}

/* ── LOGIN ── */
#login{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.login-card{background:#fff;border-radius:20px;padding:48px 44px;width:400px;
  text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.35)}
.login-logo{width:90px;height:90px;margin:0 auto 22px;border-radius:18px;overflow:hidden;
  box-shadow:0 8px 32px rgba(13,27,62,.4)}
.login-logo img{width:100%;height:100%;display:block}
.login-title{font-size:24px;font-weight:600;color:#0D1B3E;margin-bottom:4px;letter-spacing:-.5px}
.login-sub{font-size:13px;color:#888;margin-bottom:2px}
.login-by{font-size:11px;color:#bbb;margin-bottom:32px;letter-spacing:.04em;text-transform:uppercase}
.field-label{font-size:12px;color:#555;display:block;text-align:left;margin-bottom:7px;font-weight:500}
.field-input{width:100%;padding:12px 14px;border:1.5px solid #e5e7eb;border-radius:10px;
  font-size:14px;color:#111;outline:none;transition:border .15s,box-shadow .15s;letter-spacing:.5px}
.field-input:focus{border-color:#0D1B3E;box-shadow:0 0 0 3px rgba(13,27,62,.08)}
.btn-primary{width:100%;padding:13px;background:linear-gradient(135deg,#0D1B3E,#1A3560);
  color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:600;margin-top:16px;
  transition:opacity .15s,transform .1s;letter-spacing:.3px}
.btn-primary:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
.btn-primary:active{transform:translateY(0)}
.err-msg{font-size:12px;color:#e74c3c;margin-top:10px;text-align:left;display:flex;align-items:center;gap:5px}
.login-footer{font-size:11px;color:rgba(255,255,255,.25);margin-top:28px;text-align:center}

/* ── WIZARD ── */
#wizard{min-height:100vh}
.sidebar{width:230px;background:linear-gradient(180deg,#0D1B3E 0%,#0a1628 100%);
  display:flex;flex-direction:column;padding:30px 22px;flex-shrink:0;min-height:100vh}
.side-brand{display:flex;align-items:center;gap:12px;margin-bottom:36px}
.side-logo{width:40px;height:40px;border-radius:9px;overflow:hidden;flex-shrink:0}
.side-logo img{width:100%;height:100%}
.side-brand-text .side-name{font-size:16px;font-weight:700;color:#fff;letter-spacing:-.3px}
.side-brand-text .side-tag{font-size:10px;color:#4a6a9a;letter-spacing:.05em;text-transform:uppercase}
.side-steps{flex:1;display:flex;flex-direction:column;gap:4px}
.side-step{font-size:12px;color:#3a5a8a;padding:7px 10px;display:flex;align-items:center;
  gap:9px;border-radius:7px;transition:all .15s}
.side-step.done{color:#6a8fbb}
.side-step.done .side-dot{background:#2E5F9E;opacity:.6}
.side-step.active{color:#fff;background:rgba(255,255,255,.07)}
.side-step.active .side-dot{background:#4A7FBF}
.side-dot{width:6px;height:6px;border-radius:50%;background:#2a4a6a;flex-shrink:0}
.side-step.done::after{content:"✓";font-size:10px;margin-left:auto;color:#2E5F9E}
.side-bottom{padding-top:20px;border-top:1px solid #1a2d50}
.side-user{font-size:11px;color:#4a6a9a;margin-bottom:3px}
.side-user-name{font-size:13px;color:#7799cc;font-weight:500}

.main{flex:1;padding:48px 64px;display:flex;flex-direction:column;max-width:700px;overflow-y:auto}
.prog-wrap{display:flex;align-items:center;gap:14px;margin-bottom:48px}
.prog-track{flex:1;height:2px;background:#e5e7eb;border-radius:2px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#0D1B3E,#2E5F9E);
  border-radius:2px;transition:width .45s cubic-bezier(.4,0,.2,1)}
.prog-lbl{font-size:12px;color:#bbb;white-space:nowrap;font-weight:500}

.step-body{flex:1}
.step-sec{font-size:11px;color:#bbb;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;font-weight:600}
.step-q{font-size:28px;font-weight:600;line-height:1.2;margin-bottom:8px;color:#0D1B3E;letter-spacing:-.5px}
.step-hint{font-size:13px;color:#888;line-height:1.65;margin-bottom:30px}

.pills{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:30px}
.pill{padding:9px 22px;border:1.5px solid #e5e7eb;border-radius:999px;font-size:13px;
  background:#fff;color:#333;transition:all .12s;font-weight:500}
.pill:hover{border-color:#0D1B3E;color:#0D1B3E;background:#f0f3f8}
.pill.on{border:2px solid #0D1B3E;background:#0D1B3E;color:#fff}

.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(162px,1fr));gap:10px;margin-bottom:30px}
.card{border:1.5px solid #e5e7eb;border-radius:14px;padding:16px 15px 14px;background:#fff;
  text-align:left;transition:all .12s}
.card:hover{border-color:#0D1B3E;box-shadow:0 4px 16px rgba(13,27,62,.08)}
.card.on{border:2px solid #0D1B3E;background:#f0f3f8;box-shadow:0 4px 16px rgba(13,27,62,.12)}
.card-label{font-size:13px;font-weight:600;display:block;margin-bottom:5px;color:#111}
.card-sub{font-size:11px;color:#999;display:block;line-height:1.4}

.text-wrap{margin-bottom:30px}

.debt-group{margin-bottom:20px}
.debt-group-lbl{font-size:11px;color:#bbb;text-transform:uppercase;letter-spacing:.06em;margin-bottom:9px;font-weight:600}
.debt-rows{display:flex;flex-direction:column;gap:7px}
.drow{display:flex;align-items:center;gap:10px;padding:11px 15px;border:1.5px solid #e5e7eb;
  border-radius:10px;background:#fff;text-align:left;transition:all .12s}
.drow:hover{border-color:#0D1B3E}
.drow.on{border:2px solid #0D1B3E;background:#f0f3f8}
.dtog{width:18px;height:18px;border:1.5px solid #ddd;border-radius:4px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:11px;
  background:#fff;color:#aaa;transition:all .12s;font-weight:700}
.drow.on .dtog{background:#0D1B3E;border-color:#0D1B3E;color:#fff}
.dname{font-size:13px;font-weight:600;flex:1;color:#111}
.dtag{font-size:11px;color:#bbb;background:#f5f5f5;padding:2px 8px;border-radius:999px}
.drow.on .dtag{background:#d8e4f0;color:#0D1B3E}
.damt{width:100px;padding:5px 9px;border:1.5px solid #ddd;border-radius:7px;
  font-size:12px;text-align:right;display:none;background:#fff;color:#111;font-weight:500}
.drow.on .damt{display:block;border-color:#0D1B3E}

.nav{display:flex;align-items:center;justify-content:space-between;padding-top:36px;margin-top:auto}
.btn-back{background:none;border:none;font-size:13px;color:#bbb;padding:8px 0;font-weight:500}
.btn-back:hover{color:#555}
.btn-next{background:linear-gradient(135deg,#0D1B3E,#1A3560);color:#fff;border:none;
  border-radius:10px;padding:12px 28px;font-size:13px;font-weight:600;
  transition:opacity .15s,transform .1s;letter-spacing:.2px}
.btn-next:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
.btn-next:active{transform:translateY(0)}

/* Summary */
.sum-section-title{font-size:11px;color:#bbb;text-transform:uppercase;letter-spacing:.07em;
  font-weight:600;margin:20px 0 10px;padding-bottom:6px;border-bottom:1px solid #f0f0f0}
.sum-row{display:flex;justify-content:space-between;align-items:center;
  padding:9px 0;border-bottom:1px solid #f7f7f7;font-size:13px}
.sum-row:last-child{border-bottom:none}
.sum-k{color:#999;font-weight:500}
.sum-v{color:#0D1B3E;font-weight:600;text-align:right;max-width:58%}
.dpill{display:inline-flex;padding:3px 10px;border-radius:999px;background:#eef1f8;
  border:1px solid #c8d4e8;font-size:11px;color:#0D1B3E;font-weight:600;margin:2px}
.gen-err{font-size:13px;color:#e74c3c;margin-top:14px;padding:10px 14px;
  background:#fdf2f2;border-radius:8px;border:1px solid #fcd0d0}

/* ── DONE ── */
#done{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.done-card{background:#fff;border-radius:20px;padding:52px 48px;width:440px;
  text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.35)}
.done-icon{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#27ae60,#2ecc71);
  display:flex;align-items:center;justify-content:center;margin:0 auto 20px;
  font-size:32px;box-shadow:0 8px 24px rgba(39,174,96,.3)}
.done-title{font-size:24px;font-weight:600;color:#0D1B3E;margin-bottom:8px}
.done-sub{font-size:13px;color:#888;margin-bottom:8px}
.done-file{font-size:12px;color:#bbb;margin-bottom:32px;word-break:break-all;
  background:#f7f8fa;padding:8px 12px;border-radius:8px;font-family:monospace}
.btn-outline{width:100%;padding:12px;background:#fff;color:#0D1B3E;
  border:2px solid #0D1B3E;border-radius:10px;font-size:14px;font-weight:600;
  margin-top:10px;transition:background .15s}
.btn-outline:hover{background:#f0f3f8}

/* Spinner */
.spinner{display:inline-block;width:15px;height:15px;border:2px solid rgba(255,255,255,.3);
  border-top-color:#fff;border-radius:50%;animation:spin .65s linear infinite;
  vertical-align:middle;margin-right:8px}
@keyframes spin{to{transform:rotate(360deg)}}
.fade-in{animation:fi .25s ease}
@keyframes fi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* ── IMPORT SCREEN ── */
#import-screen{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.import-card{background:#fff;border-radius:20px;padding:48px 44px;width:560px;
  box-shadow:0 24px 80px rgba(0,0,0,.35)}
.import-header{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.import-logo{width:44px;height:44px;border-radius:10px;overflow:hidden;flex-shrink:0}
.import-logo img{width:100%;height:100%}
.import-title{font-size:22px;font-weight:600;color:#0D1B3E;letter-spacing:-.4px}
.import-sub{font-size:13px;color:#888;margin-top:2px}
.drop-zone{border:2px dashed #d0d8e8;border-radius:14px;padding:40px 24px;text-align:center;
  cursor:pointer;transition:all .2s;background:#fafbfc;margin-bottom:20px;position:relative}
.drop-zone:hover,.drop-zone.drag{border-color:#0D1B3E;background:#f0f3f8}
.drop-zone input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.drop-icon{font-size:36px;margin-bottom:12px}
.drop-title{font-size:15px;font-weight:600;color:#0D1B3E;margin-bottom:6px}
.drop-sub{font-size:12px;color:#aaa;line-height:1.6}
.drop-formats{display:flex;gap:6px;justify-content:center;margin-top:12px;flex-wrap:wrap}
.fmt-badge{padding:3px 10px;border-radius:999px;background:#eef1f8;border:1px solid #c8d4e8;
  font-size:11px;color:#0D1B3E;font-weight:600}
.import-file-info{display:none;align-items:center;gap:10px;padding:12px 16px;
  background:#f0f8f0;border:1.5px solid #27ae60;border-radius:10px;margin-bottom:16px}
.import-file-info.show{display:flex}
.file-icon{font-size:20px}
.file-name{font-size:13px;font-weight:600;color:#1a6b3a;flex:1}
.file-size{font-size:11px;color:#888}
.quality-panel{display:none;border-radius:12px;padding:18px 20px;margin-bottom:20px;border:1.5px solid}
.quality-panel.show{display:block}
.quality-panel.excellent{background:#f0faf4;border-color:#27ae60}
.quality-panel.bon{background:#f0f6ff;border-color:#2E5F9E}
.quality-panel.partiel{background:#fffbf0;border-color:#f39c12}
.quality-panel.insuffisant{background:#fff5f5;border-color:#e74c3c}
.quality-title{font-size:13px;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.quality-score{font-size:22px;font-weight:700}
.quality-items{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.q-item{display:flex;align-items:center;gap:5px;font-size:11px;padding:3px 9px;
  border-radius:999px;font-weight:500}
.q-item.ok{background:#d4edda;color:#1a6b3a}
.q-item.miss{background:#fce8e6;color:#c0392b}
.actuals-preview{display:none;margin-bottom:20px}
.actuals-preview.show{display:block}
.preview-title{font-size:12px;font-weight:600;color:#555;text-transform:uppercase;
  letter-spacing:.06em;margin-bottom:10px}
.preview-table{width:100%;border-collapse:collapse;font-size:12px}
.preview-table th{background:#f5f7fa;color:#888;font-weight:600;padding:6px 10px;
  text-align:right;font-size:11px;border-bottom:1px solid #eee}
.preview-table th:first-child{text-align:left}
.preview-table td{padding:7px 10px;border-bottom:1px solid #f5f5f5;color:#333}
.preview-table td:first-child{font-weight:500;color:#0D1B3E}
.preview-table td:not(:first-child){text-align:right;font-family:monospace;font-size:11px}
.preview-table tr:hover td{background:#fafafa}
.import-actions{display:flex;gap:10px;margin-top:4px}
.btn-secondary{flex:1;padding:12px;background:#f5f7fa;color:#0D1B3E;border:1.5px solid #d0d8e8;
  border-radius:10px;font-size:13px;font-weight:600;transition:all .15s}
.btn-secondary:hover{background:#e8edf5;border-color:#0D1B3E}
.import-err{font-size:13px;color:#e74c3c;padding:10px 14px;background:#fdf2f2;
  border-radius:8px;border:1px solid #fcd0d0;margin-bottom:14px;display:none}
.import-err.show{display:block}
.skip-link{text-align:center;margin-top:16px}
.skip-link button{background:none;border:none;font-size:12px;color:#bbb;text-decoration:underline;cursor:pointer}
.skip-link button:hover{color:#888}

/* ── SCENARIOS SCREEN ── */
#scenarios-screen{align-items:flex-start;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%);
  padding:32px 24px;overflow-y:auto}
.sc-wrap{width:100%;max-width:1100px;margin:0 auto}
.sc-top-bar{display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.06);
  border-radius:16px;padding:18px 24px;margin-bottom:24px;backdrop-filter:blur(8px)}
.sc-logo-sm{width:38px;height:38px;border-radius:9px;overflow:hidden;flex-shrink:0}
.sc-logo-sm img{width:100%;height:100%}
.sc-top-title{font-size:18px;font-weight:700;color:#fff;letter-spacing:-.3px}
.sc-top-sub{font-size:12px;color:#7799cc;margin-top:2px}
.sc-top-actions{margin-left:auto;display:flex;gap:10px}
.btn-sc-back{background:rgba(255,255,255,.1);color:#fff;border:none;border-radius:8px;
  padding:9px 18px;font-size:13px;font-weight:500;cursor:pointer;transition:background .15s;font-family:inherit}
.btn-sc-back:hover{background:rgba(255,255,255,.18)}
.btn-sc-gen{background:#fff;color:#0D1B3E;border:none;border-radius:8px;
  padding:9px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:opacity .15s;font-family:inherit}
.btn-sc-gen:hover:not(:disabled){opacity:.88}
.btn-sc-gen:disabled{opacity:.4;cursor:not-allowed}

/* 3-column grid */
.sc-grid{display:grid;grid-template-columns:200px 1fr 1fr 1fr;gap:0;
  background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 12px 48px rgba(0,0,0,.3)}
.sc-grid-header{display:contents}
.sc-col-label{background:#f8f9fa;border-right:1px solid #eee}
.sc-col-low{background:#fff5f5}
.sc-col-base{background:#f0f3f8}
.sc-col-best{background:#f0faf4}
.sc-col-head{padding:16px 14px;text-align:center;font-size:13px;font-weight:700;
  border-bottom:3px solid;display:flex;flex-direction:column;align-items:center;gap:4px}
.sc-col-head.label{background:#f8f9fa;border-color:#e0e0e0;text-align:left;
  justify-content:flex-end;font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:.06em}
.sc-col-head.low{border-color:#e74c3c;color:#c0392b;background:#fff5f5}
.sc-col-head.base{border-color:#0D1B3E;color:#0D1B3E;background:#eef1f8}
.sc-col-head.best{border-color:#27ae60;color:#27ae60;background:#f0faf4}
.sc-col-head .sc-icon{font-size:20px}
.sc-col-head .sc-head-label{font-size:14px}
.sc-col-head .sc-head-sub{font-size:10px;font-weight:400;opacity:.7}

/* Section rows */
.sc-section-row{display:contents}
.sc-section-cell{padding:10px 14px;font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:.07em;color:#fff;grid-column:1/-1;
  border-top:2px solid rgba(0,0,0,.05)}
.sc-section-cell.pl{background:#1A3560}
.sc-section-cell.nwc{background:#7B3F00}
.sc-section-cell.capex{background:#2C4A6E}
.sc-section-cell.debt{background:#7B0000}
.sc-section-cell.macro{background:#0D3349}

/* Param rows */
.sc-param-row{display:contents}
.sc-param-row:hover .sc-cell{background:#fafbfc}
.sc-param-row:hover .sc-cell.low{background:#fff0f0}
.sc-param-row:hover .sc-cell.base{background:#e8edf5}
.sc-param-row:hover .sc-cell.best{background:#e8f5ec}
.sc-cell{padding:8px 14px;border-bottom:1px solid #f0f0f0;display:flex;
  align-items:center;font-size:13px}
.sc-cell.label{color:#444;font-weight:500;border-right:1px solid #eee;
  justify-content:space-between}
.sc-cell .sc-unit{font-size:10px;color:#bbb;margin-left:4px}
.sc-cell.low{background:#fff5f5}
.sc-cell.base{background:#f0f3f8}
.sc-cell.best{background:#f0faf4}

/* Inputs */
.sc-input{width:100%;padding:5px 8px;border:1.5px solid transparent;border-radius:6px;
  font-size:13px;font-family:inherit;background:transparent;color:#111;
  text-align:right;transition:border .12s,background .12s;font-weight:500}
.sc-input:focus{outline:none;background:#fff;border-color:#0D1B3E}
.sc-cell.low .sc-input:focus{border-color:#e74c3c;background:#fff}
.sc-cell.best .sc-input:focus{border-color:#27ae60;background:#fff}
.sc-input.changed{font-weight:700}
.sc-input.low-val{color:#c0392b}
.sc-input.best-val{color:#27ae60}

/* Results */
.sc-results-bar{background:rgba(255,255,255,.06);border-radius:12px;
  padding:18px 24px;margin-top:20px;display:none}
.sc-results-bar.show{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.sc-results-title{font-size:13px;color:#fff;font-weight:600;margin-right:4px}
.sc-result-pill{display:flex;align-items:center;gap:8px;padding:8px 16px;
  border-radius:999px;font-size:12px;font-weight:600;cursor:pointer;
  border:none;font-family:inherit;transition:opacity .15s}
.sc-result-pill:hover{opacity:.85}
.sc-result-pill.low{background:#e74c3c;color:#fff}
.sc-result-pill.base{background:#fff;color:#0D1B3E}
.sc-result-pill.best{background:#27ae60;color:#fff}
.sc-err{background:rgba(231,76,60,.15);color:#ff8877;border-radius:8px;
  padding:10px 16px;font-size:13px;margin-top:12px;display:none}
.sc-err.show{display:block}

/* ── PREVIEW SCREEN ── */
#preview-screen{align-items:flex-start;justify-content:center;min-height:100vh;
  background:#f0f2f5;padding:0}
.pv-layout{display:flex;min-height:100vh;width:100%}
.pv-sidebar{width:200px;background:#0D1B3E;display:flex;flex-direction:column;
  padding:24px 18px;flex-shrink:0;min-height:100vh}
.pv-side-logo{width:38px;height:38px;border-radius:9px;overflow:hidden;margin-bottom:8px}
.pv-side-logo img{width:100%;height:100%}
.pv-side-title{font-size:15px;font-weight:700;color:#fff;margin-bottom:4px}
.pv-side-company{font-size:11px;color:#7799cc;margin-bottom:28px;word-break:break-word}
.pv-nav-item{display:flex;align-items:center;gap:8px;padding:9px 10px;border-radius:8px;
  cursor:pointer;font-size:12px;color:#4a6a9a;transition:all .15s;margin-bottom:3px;
  border:none;background:none;font-family:inherit;width:100%;text-align:left}
.pv-nav-item:hover{background:rgba(255,255,255,.06);color:#aac4e8}
.pv-nav-item.active{background:rgba(255,255,255,.1);color:#fff;font-weight:600}
.pv-nav-dot{width:6px;height:6px;border-radius:50%;background:currentColor;flex-shrink:0}
.pv-side-actions{margin-top:auto;display:flex;flex-direction:column;gap:8px}
.btn-pv-dl{padding:9px 12px;background:linear-gradient(135deg,#0D1B3E,#1A3560);
  color:#fff;border:none;border-radius:8px;font-size:12px;font-weight:600;
  cursor:pointer;font-family:inherit;transition:opacity .15s}
.btn-pv-dl:hover{opacity:.85}
.btn-pv-back{padding:8px 12px;background:rgba(255,255,255,.08);color:#aac4e8;
  border:none;border-radius:8px;font-size:12px;cursor:pointer;font-family:inherit}
.btn-pv-back:hover{background:rgba(255,255,255,.15)}

.pv-main{flex:1;padding:32px 40px;overflow-y:auto}
.pv-header{margin-bottom:24px}
.pv-title{font-size:22px;font-weight:700;color:#0D1B3E;letter-spacing:-.4px;margin-bottom:4px}
.pv-subtitle{font-size:13px;color:#888}
.pv-tabs{display:flex;gap:4px;margin-bottom:20px;border-bottom:2px solid #e5e7eb;padding-bottom:0}
.pv-tab{padding:9px 20px;font-size:13px;font-weight:500;color:#888;cursor:pointer;
  border:none;background:none;font-family:inherit;border-bottom:2px solid transparent;
  margin-bottom:-2px;transition:all .15s}
.pv-tab:hover{color:#0D1B3E}
.pv-tab.active{color:#0D1B3E;font-weight:700;border-bottom-color:#0D1B3E}

/* Preview table */
.pv-table-wrap{background:#fff;border-radius:14px;overflow:hidden;
  box-shadow:0 2px 16px rgba(0,0,0,.06);margin-bottom:20px}
.pv-table{width:100%;border-collapse:collapse;font-size:12px}
.pv-table th{background:#0D1B3E;color:#fff;font-weight:600;padding:10px 14px;
  text-align:right;font-size:11px;letter-spacing:.04em;white-space:nowrap}
.pv-table th:first-child{text-align:left;width:220px}
.pv-table td{padding:8px 14px;border-bottom:1px solid #f5f5f5;color:#333;
  text-align:right;white-space:nowrap}
.pv-table td:first-child{text-align:left;color:#444;padding-left:14px}
.pv-table tr.pv-section td{background:#1A3560;color:#fff;font-size:11px;
  font-weight:700;text-transform:uppercase;letter-spacing:.07em;padding:6px 14px}
.pv-table tr.pv-total td{background:#eef1f8;font-weight:700;color:#0D1B3E;
  border-top:1px solid #c8d4e8}
.pv-table tr.pv-total td:first-child{padding-left:14px}
.pv-table tr:hover:not(.pv-section):not(.pv-total) td{background:#fafbfc}
.pv-table td.pv-neg{color:#c0392b}
.pv-table td.pv-pos{color:#27ae60}
.pv-table td.pv-pct{font-size:11px;color:#666}

/* Summary cards */
.pv-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
  gap:12px;margin-bottom:24px}
.pv-card{background:#fff;border-radius:12px;padding:16px 18px;
  box-shadow:0 2px 12px rgba(0,0,0,.06)}
.pv-card-label{font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:.05em;
  margin-bottom:6px;font-weight:600}
.pv-card-value{font-size:22px;font-weight:700;color:#0D1B3E;letter-spacing:-.5px}
.pv-card-unit{font-size:11px;color:#bbb;margin-left:3px}
.pv-card-delta{font-size:11px;margin-top:4px;font-weight:500}
.pv-card-delta.pos{color:#27ae60}
.pv-card-delta.neg{color:#c0392b}

.pv-loading{display:flex;align-items:center;justify-content:center;
  padding:60px;color:#aaa;font-size:14px;gap:12px}

</style>
</head>
<body>
<div id="app">

<!-- LOGIN -->
<div id="login" class="screen active">
  <div class="login-card">
    <div class="login-logo"><img src="/assets/icon_256.png" alt="MG"></div>
    <div class="login-title">BP Generator</div>
    <div class="login-sub">Professional Business Plan Builder</div>
    <div class="login-by">by JRC Corporate Consulting</div>
    <label class="field-label">Code d'accès</label>
    <input id="license-input" class="field-input" type="text" placeholder="JRC-XXXX-XXXX" autocomplete="off">
    <div id="login-err" class="err-msg" style="display:none">⚠ <span id="err-text"></span></div>
    <button class="btn-primary" id="btn-login">Accéder à l'application →</button>
  </div>
  <div class="login-footer">© 2025 JRC Corporate Consulting — DIFC, Dubai</div>
</div>


<!-- IMPORT SCREEN -->
<div id="import-screen" class="screen">
  <div class="import-card">
    <div class="import-header">
      <div class="import-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div>
        <div class="import-title">Importer les données financières</div>
        <div class="import-sub">Excel, CSV ou PDF — les actuals pré-rempliront le modèle</div>
      </div>
    </div>

    <div class="drop-zone" id="drop-zone">
      <input type="file" id="file-input" accept=".xlsx,.xls,.xlsm,.csv,.txt,.tsv,.pdf">
      <div class="drop-icon">📂</div>
      <div class="drop-title">Glisse ton fichier ici ou clique pour parcourir</div>
      <div class="drop-sub">P&L, Bilan, Cash Flow — n'importe quelle structure<br>Le moteur reconnaît automatiquement les lignes financières</div>
      <div class="drop-formats">
        <span class="fmt-badge">Excel .xlsx</span>
        <span class="fmt-badge">CSV</span>
        <span class="fmt-badge">PDF</span>
      </div>
    </div>

    <div class="import-file-info" id="file-info">
      <span class="file-icon">📄</span>
      <span class="file-name" id="file-name-lbl"></span>
      <span class="file-size" id="file-size-lbl"></span>
    </div>

    <div class="import-err" id="import-err"></div>

    <div class="quality-panel" id="quality-panel">
      <div class="quality-title">
        <span id="quality-label"></span>
        <span class="quality-score" id="quality-score"></span>
        <span style="font-size:12px;color:#888;font-weight:400">/ 100</span>
      </div>
      <div class="quality-items" id="quality-items"></div>
    </div>

    <div class="actuals-preview" id="actuals-preview">
      <div class="preview-title">Aperçu des données extraites</div>
      <table class="preview-table" id="preview-table">
        <thead id="preview-head"></thead>
        <tbody id="preview-body"></tbody>
      </table>
    </div>

    <div class="import-actions">
      <button class="btn-secondary" id="btn-reupload" style="display:none">↩ Changer de fichier</button>
      <button class="btn-primary" id="btn-use-data" style="display:none">Utiliser ces données → Configurer le BP</button>
    </div>
    <button class="btn-primary" id="btn-analyze" style="display:none;width:100%;margin-top:0">Analyser le fichier →</button>

    <div class="skip-link">
      <button id="btn-skip-import">Passer cette étape — saisir les données manuellement</button>
    </div>
  </div>
</div>

<!-- WIZARD -->
<div id="wizard" class="screen">
  <div class="sidebar">
    <div class="side-brand">
      <div class="side-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div class="side-brand-text">
        <div class="side-name">BP Generator</div>
        <div class="side-tag">JRC Corporate</div>
      </div>
    </div>
    <div class="side-steps" id="side-steps"></div>
    <div class="side-bottom">
      <div class="side-user">Connecté en tant que</div>
      <div class="side-user-name" id="side-user-name">—</div>
    </div>
  </div>
  <div class="main">
    <div class="prog-wrap">
      <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
      <div class="prog-lbl" id="prog-lbl"></div>
    </div>
    <div id="step-content" class="step-body fade-in"></div>
    <div class="nav">
      <button class="btn-back" id="btn-back">← Retour</button>
      <button class="btn-next" id="btn-next">Suivant →</button>
    </div>
  </div>
</div>

<!-- DONE -->
<div id="done" class="screen">
  <div class="done-card">
    <div class="done-icon">✓</div>
    <div class="done-title">Modèle généré !</div>
    <div class="done-sub">Ton fichier Excel est prêt</div>
    <div class="done-file" id="done-filename"></div>
    <button class="btn-primary" id="btn-download">⬇ Télécharger le fichier Excel</button>
    <button class="btn-primary" id="btn-preview" onclick="loadPreview(currentFilename)" style="background:linear-gradient(135deg,#2E5F9E,#1A3560)">👁 Voir l'aperçu du modèle</button>
      <button class="btn-primary" id="btn-scenarios" onclick="showScreen('scenarios-screen')" style="background:linear-gradient(135deg,#27ae60,#2ecc71);margin-top:0">📊 Générer Low / Base / Best Case</button>
      <button class="btn-outline" id="btn-new">+ Nouveau modèle</button>
  </div>
</div>

</div>
<script>
const API='';let licenseKey='',currentUser='',currentFilename='';
const STEPS=[
  {id:'name',sec:'Identité',q:'Quel est le nom de la société ou du projet ?',hint:"Tel qu'il apparaîtra en en-tête de chaque onglet Excel.",type:'text',f:'company_name',ph:'ex. JBF Global Europe — Industrial BP'},
  {id:'type',sec:'Type de modèle',q:'Quel type de business plan ?',hint:'Détermine les drivers de revenus et la structure du modèle.',type:'cards',f:'business_type',multi:false,opts:[
    {v:'industrial',l:'Industriel',s:'Volume MT, spread, capacité'},{v:'lbo',l:'LBO / M&A',s:'Leveraged buyout, IRR/MOIC'},
    {v:'saas',l:'SaaS / Tech',s:'ARR, churn, LTV/CAC'},{v:'immo',l:'Immobilier',s:'Loyers/m², LTV, rendement'},
    {v:'restr',l:'Restructuring',s:'SSFA, haircut, PIK, covenants'},{v:'retail',l:'Retail',s:'Magasins, panier moyen, SSS'}]},
  {id:'ccy',sec:'Paramètres',q:'Devise de reporting ?',type:'pills',f:'currency',multi:false,opts:['USD','EUR','GBP','AED','BHD','SAR']},
  {id:'yrs',sec:'Paramètres',q:'Horizon de projection ?',hint:"Nombre d'années de business plan.",type:'pills',f:'n_years',multi:false,opts:['3 ans','5 ans','7 ans','10 ans']},
  {id:'fy',sec:'Paramètres',q:"Mois de début d'exercice fiscal ?",hint:'Janvier = calendaire. Avril = fiscal UK/Bahreïn.',type:'pills',f:'fy_start_month',multi:false,opts:['Janvier','Février','Mars','Avril','Juillet','Octobre']},
  {id:'mods',sec:'Modules',q:'Quels modules inclure ?',hint:'P&L, BS et CF sont toujours actifs.',type:'cards',f:'modules',multi:true,opts:[
    {v:'debt',l:'Debt schedule',s:'Multi-tranche, covenants, sweep'},{v:'nwc',l:'NWC',s:'DSO / DIO / DPO'},
    {v:'capex',l:'CAPEX',s:"Plan d'invest. & amortissements"},{v:'tax',l:'Fiscalité',s:'IS, impôt différé, déficits'},
    {v:'scenarios',l:'Scénarios',s:'Low / Base / High'},{v:'returns',l:'Returns / LBO',s:'IRR, MOIC, waterfall equity'},
    {v:'valuation',l:'Valorisation',s:'DCF + EV/EBITDA exit bridge'},{v:'consol',l:'Consolidation',s:'Multi-entités + éliminations'}]},
  {id:'debt',sec:'Financement',q:'Quelles tranches de dette activer ?',hint:'Coche chaque tranche et saisis le montant en milliers.',type:'debt',f:'debt',groups:[
    {lbl:'Senior sécurisée',items:[{k:'tla',l:'Term Loan A',t:'Amortissable',d:150000},{k:'tlb',l:'Term Loan B',t:'Bullet',d:0},{k:'ss',l:'Super Senior (SSFA)',t:'Prioritaire',d:0},{k:'rcf',l:'RCF',t:'Revolving',d:40000},{k:'mur',l:'Murabaha islamique',t:'Islamic',d:0}]},
    {lbl:'Mezzanine / Subordonné',items:[{k:'mez',l:'Mezzanine cash pay',t:'Mezz',d:0},{k:'pik',l:'PIK toggle',t:'PIK',d:0},{k:'shl',l:'SHL (shareholder)',t:'Full PIK',d:0},{k:'uni',l:'Unitranche',t:'Blended',d:0}]},
    {lbl:'Capital markets / Restructuring',items:[{k:'hyb',l:'High Yield Bond',t:'HYB',d:0},{k:'dip',l:'New money (DIP-style)',t:'Super senior',d:0},{k:'d2e',l:'Debt-to-equity swap',t:'Haircut',d:0}]}]},
  {id:'mech',sec:'Mécaniques',q:'Quelles mécaniques de dette activer ?',type:'cards',f:'mechanics',multi:true,opts:[
    {v:'sweep',l:'Cash sweep',s:'Remboursement sur FCF excédentaire'},{v:'ratchet',l:'Margin ratchet',s:'Marge liée au niveau de levier'},
    {v:'cov',l:'Covenant tracking',s:'Levier, ICR, DSCR + flags'},{v:'oid',l:'OID / upfront fees',s:'Amortissement sur durée'},
    {v:'fx',l:'Couverture FX',s:'Multi-devise par tranche'},{v:'irs',l:'Swap taux fixe/flottant',s:'Interest rate swap'}]},
  {id:'rate',sec:'Mécaniques',q:'Quel taux de référence ?',type:'pills',f:'base_rate_index',multi:false,opts:['SOFR','EURIBOR 3M','EURIBOR 6M','SONIA','Taux fixe']},
  {id:'fmt',sec:'Format',q:'Granularité du modèle ?',type:'cards',f:'output_format',multi:false,opts:[
    {v:'annual',l:'Annuel uniquement',s:'Standard IM boutique, plus lisible'},{v:'monthly',l:'Mensuel + annuel',s:'Détail opérationnel complet'},{v:'quarterly',l:'Trimestriel + annuel',s:'Fréquence intermédiaire'}]},
  {id:'sum',sec:'Récapitulatif',q:'Tout est bon ?',hint:'Vérifie la configuration avant de lancer la génération.',type:'summary'}
];
const YRS={'3 ans':3,'5 ans':5,'7 ans':7,'10 ans':10};
const MNTH={'Janvier':1,'Février':2,'Mars':3,'Avril':4,'Juillet':7,'Octobre':10};
let answers={},stepIdx=0;
function visibleSteps(){const h=(answers.modules||[]).includes('debt');return STEPS.filter(s=>(['debt','mech','rate'].includes(s.id)?h:true));}
document.getElementById('btn-login').onclick=doLogin;
document.getElementById('license-input').onkeydown=e=>e.key==='Enter'&&doLogin();
async function doLogin(){
  const key=document.getElementById('license-input').value.trim();
  const errEl=document.getElementById('login-err');const errTxt=document.getElementById('err-text');
  const btn=document.getElementById('btn-login');
  if(!key)return;
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Vérification...';
  errEl.style.display='none';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({license_key:key})});
    const d=await r.json();if(!r.ok)throw new Error(d.detail||'Erreur');
    licenseKey=key;currentUser=d.user;
    document.getElementById('side-user-name').textContent=d.user;
    showScreen('wizard');renderStep();
  }catch(e){errTxt.textContent=e.message;errEl.style.display='flex';}
  btn.disabled=false;btn.textContent='Accéder à l\'application →';}
function showScreen(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active');}
document.getElementById('btn-next').onclick=onNext;
document.getElementById('btn-back').onclick=onBack;
function onNext(){const vs=visibleSteps();const s=vs[stepIdx];if(s.type==='summary'){doGenerate();return;}if(stepIdx<vs.length-1){stepIdx++;renderStep();}}
function onBack(){if(stepIdx>0){stepIdx--;renderStep();}}
function renderStep(){
  const vs=visibleSteps();const s=vs[stepIdx];const pct=Math.round((stepIdx/(vs.length-1))*100);
  document.getElementById('prog-fill').style.width=pct+'%';
  document.getElementById('prog-lbl').textContent=(stepIdx+1)+' / '+vs.length;
  document.getElementById('btn-back').style.visibility=stepIdx===0?'hidden':'visible';
  const nb=document.getElementById('btn-next');
  nb.textContent=s.type==='summary'?'Générer le modèle Excel →':'Suivant →';
  nb.disabled=!canAdvance(s);
  document.getElementById('side-steps').innerHTML=vs.map((st,i)=>
    `<div class="side-step ${i<stepIdx?'done':i===stepIdx?'active':''}">`+
    '<div class="side-dot"></div>'+st.sec+'</div>').join('');
  const el=document.getElementById('step-content');
  el.className='step-body fade-in';void el.offsetWidth;
  el.innerHTML=buildHTML(s);attachEvents(s);
  if(s.type==='text'){const inp=el.querySelector('input');if(inp){inp.focus();inp.oninput=()=>{answers[s.f]=inp.value;nb.disabled=!inp.value.trim();};inp.onkeydown=e=>e.key==='Enter'&&!nb.disabled&&onNext();}}}
function canAdvance(s){
  if(s.type==='text')return!!(answers[s.f]||'').trim();
  if(['summary','debt'].includes(s.type))return true;
  if(s.multi)return(answers[s.f]||[]).length>0;
  return!!answers[s.f];}
function buildHTML(s){
  const sec=`<div class="step-sec">${s.sec}</div>`;
  const q=`<div class="step-q">${s.q}</div>`;
  const hint=s.hint?`<div class="step-hint">${s.hint}</div>`:'';
  if(s.type==='text')return sec+q+hint+`<div class="text-wrap"><input class="field-input" id="txt" value="${answers[s.f]||''}" placeholder="${s.ph||''}" style="font-size:15px;padding:13px 15px"></div>`;
  if(s.type==='pills'){const cur=answers[s.f];return sec+q+hint+'<div class="pills">'+s.opts.map(o=>`<button class="pill${cur===o?' on':''}" data-v="${o}">${o}</button>`).join('')+'</div>';}
  if(s.type==='cards'){const cur=answers[s.f]||(s.multi?[]:null);return sec+q+hint+'<div class="cards">'+s.opts.map(o=>{const sel=s.multi?(cur||[]).includes(o.v):cur===o.v;return`<button class="card${sel?' on':''}" data-v="${o.v}"><span class="card-label">${o.l}</span><span class="card-sub">${o.s}</span></button>`;}).join('')+'</div>';}
  if(s.type==='debt'){const cur=answers.debt||{};return sec+q+hint+s.groups.map(g=>'<div class="debt-group"><div class="debt-group-lbl">'+g.lbl+'</div><div class="debt-rows">'+g.items.map(item=>{const on=cur[item.k]!==undefined;return`<button class="drow${on?' on':''}" data-k="${item.k}" data-d="${item.d}"><div class="dtog">${on?'✓':''}</div><span class="dname">${item.l}</span><span class="dtag">${item.t}</span><input class="damt" type="number" value="${on?cur[item.k]:item.d}" placeholder="Montant k" min="0" step="1000"></button>`;}).join('')+'</div></div>').join('');}
  if(s.type==='summary'){
    const d=answers;const debt=d.debt||{};
    const dp=Object.entries(debt).map(([k,v])=>`<span class="dpill">${k.toUpperCase()} — ${Number(v).toLocaleString()}k</span>`).join('')||'<span style="color:#bbb;font-size:12px">Aucune tranche</span>';
    return sec+q+hint+
      '<div class="sum-section-title">Identité & horizon</div>'+
      [['Société',d.company_name],['Type',d.business_type],['Devise',d.currency],['Horizon',d.n_years],['Exercice fiscal',d.fy_start_month]].map(([k,v])=>`<div class="sum-row"><span class="sum-k">${k}</span><span class="sum-v">${v||'—'}</span></div>`).join('')+
      '<div class="sum-section-title">Modules & format</div>'+
      [['Modules',(d.modules||[]).join(', ')||'—'],['Mécaniques',(d.mechanics||[]).join(', ')||'—'],['Taux de ref.',d.base_rate_index],['Format',d.output_format]].map(([k,v])=>`<div class="sum-row"><span class="sum-k">${k}</span><span class="sum-v">${v||'—'}</span></div>`).join('')+
      '<div class="sum-section-title">Tranches de dette</div>'+
      `<div style="padding:8px 0">${dp}</div>`+
      '<div id="gen-err" class="gen-err" style="display:none"></div>';
  }return'';}
function attachEvents(s){
  const nb=document.getElementById('btn-next');
  if(s.type==='pills')document.querySelectorAll('.pill').forEach(b=>{b.onclick=()=>{document.querySelectorAll('.pill').forEach(x=>x.classList.remove('on'));b.classList.add('on');answers[s.f]=b.dataset.v;nb.disabled=false;};});
  if(s.type==='cards')document.querySelectorAll('.card').forEach(b=>{b.onclick=()=>{if(s.multi){b.classList.toggle('on');answers[s.f]=[...document.querySelectorAll('.card.on')].map(x=>x.dataset.v);nb.disabled=(answers[s.f]||[]).length===0;}else{document.querySelectorAll('.card').forEach(x=>x.classList.remove('on'));b.classList.add('on');answers[s.f]=b.dataset.v;nb.disabled=false;}};});
  if(s.type==='debt')document.querySelectorAll('.drow').forEach(row=>{
    row.onclick=e=>{if(e.target.tagName==='INPUT')return;const k=row.dataset.k;const def=parseInt(row.dataset.d)||0;const cur=answers.debt||{};if(cur[k]!==undefined){const n={...cur};delete n[k];answers.debt=n;row.classList.remove('on');row.querySelector('.dtog').textContent='';}else{const inp=row.querySelector('.damt');answers.debt={...cur,[k]:inp?parseInt(inp.value)||def:def};row.classList.add('on');row.querySelector('.dtog').textContent='✓';}};
    const inp=row.querySelector('.damt');if(inp)inp.oninput=e=>{e.stopPropagation();const k=row.dataset.k;if(answers.debt&&answers.debt[k]!==undefined)answers.debt[k]=parseInt(inp.value)||0;};});}
async function doGenerate(){
  const btn=document.getElementById('btn-next');const errEl=document.getElementById('gen-err');
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Génération en cours...';
  if(errEl)errEl.style.display='none';
  const payload={company_name:answers.company_name||'Business Plan',business_type:answers.business_type||'industrial',currency:answers.currency||'USD',n_years:YRS[answers.n_years]||7,fy_start_month:MNTH[answers.fy_start_month]||1,modules:answers.modules||[],debt:answers.debt||{},mechanics:answers.mechanics||[],base_rate_index:answers.base_rate_index||'SOFR',output_format:answers.output_format||'annual'};
  try{
    const r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json','x-license':licenseKey},body:JSON.stringify(payload)});
    const d=await r.json();if(!r.ok)throw new Error(d.detail||'Erreur génération');
    currentFilename=d.filename;document.getElementById('done-filename').textContent=d.filename;showScreen('done');
  }catch(e){if(errEl){errEl.textContent='⚠ '+e.message;errEl.style.display='block';}btn.disabled=false;btn.textContent='Générer le modèle Excel →';}
}
document.getElementById('btn-download').onclick=()=>{
  fetch(`/api/download/${currentFilename}`,{headers:{'x-license':licenseKey}}).then(r=>r.blob()).then(blob=>{const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=currentFilename;document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);});};
document.getElementById('btn-new').onclick=()=>{answers={};stepIdx=0;showScreen('wizard');renderStep();};

// ── IMPORT MODULE ─────────────────────────────────────────────────────────────
let importedData = null;
let selectedFile = null;

const dropZone  = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

// Drag and drop
dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('drag'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('drag');
  const f = e.dataTransfer.files[0];
  if (f) handleFileSelect(f);
});
fileInput.addEventListener('change', e => {
  if (e.target.files[0]) handleFileSelect(e.target.files[0]);
});

function handleFileSelect(file) {
  selectedFile = file;
  const info = document.getElementById('file-info');
  document.getElementById('file-name-lbl').textContent = file.name;
  document.getElementById('file-size-lbl').textContent = (file.size/1024).toFixed(1) + ' KB';
  info.classList.add('show');
  document.getElementById('btn-analyze').style.display = 'block';
  document.getElementById('btn-reupload').style.display = 'none';
  document.getElementById('btn-use-data').style.display = 'none';
  document.getElementById('quality-panel').classList.remove('show');
  document.getElementById('actuals-preview').classList.remove('show');
  document.getElementById('import-err').classList.remove('show');
}

document.getElementById('btn-analyze').onclick = async () => {
  if (!selectedFile) return;
  const btn = document.getElementById('btn-analyze');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Analyse en cours...';

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const r = await fetch('/api/import', {
      method: 'POST',
      headers: { 'x-license': licenseKey },
      body: formData,
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur extraction');

    importedData = d;
    showQualityPanel(d.data_quality);
    showActualsPreview(d.actuals_overlay, d.hist_years);

    document.getElementById('btn-analyze').style.display = 'none';
    document.getElementById('btn-reupload').style.display = 'block';
    document.getElementById('btn-use-data').style.display = 'block';
  } catch(e) {
    const errEl = document.getElementById('import-err');
    errEl.textContent = '⚠ ' + e.message;
    errEl.classList.add('show');
  }
  btn.disabled = false;
  btn.innerHTML = 'Analyser le fichier →';
};

function showQualityPanel(q) {
  const panel = document.getElementById('quality-panel');
  panel.className = 'quality-panel show ' + q.label.toLowerCase();
  document.getElementById('quality-label').textContent = 'Qualité des données : ' + q.label;
  document.getElementById('quality-score').textContent = q.score;

  const coreKeys = ['revenue','ebitda','net_income','gross_profit','ebit',
                    'depreciation','gross_debt','cash','capex','operating_cf'];
  const labels = {
    revenue:'Revenus', ebitda:'EBITDA', net_income:'Résultat net',
    gross_profit:'Marge brute', ebit:'EBIT', depreciation:'D&A',
    gross_debt:'Dette brute', cash:'Trésorerie', capex:'Capex',
    operating_cf:'Cash opérationnel', trade_receivables:'Créances clients',
    inventories:'Stocks', trade_payables:'Dettes fourn.'
  };
  const items = document.getElementById('quality-items');
  items.innerHTML = '';
  for (const [key, present] of Object.entries(q.present)) {
    if (!coreKeys.includes(key) && !['trade_receivables','inventories','trade_payables'].includes(key)) continue;
    const span = document.createElement('span');
    span.className = 'q-item ' + (present ? 'ok' : 'miss');
    span.textContent = (present ? '✓ ' : '✗ ') + (labels[key] || key);
    items.appendChild(span);
  }
}

function fmt(v) {
  if (v === null || v === undefined) return '—';
  const n = parseFloat(v);
  if (isNaN(n)) return '—';
  if (Math.abs(n) >= 1000000) return (n/1000000).toFixed(1) + 'M';
  if (Math.abs(n) >= 1000)    return (n/1000).toFixed(0) + 'k';
  return n.toFixed(1);
}

function showActualsPreview(actuals, years) {
  const preview = document.getElementById('actuals-preview');
  const thead = document.getElementById('preview-head');
  const tbody = document.getElementById('preview-body');

  const rowLabels = {
    revenue:'Revenus', gross_profit:'Marge brute', ebitda:'EBITDA',
    ebitda_margin:'Marge EBITDA %', ebit:'EBIT', net_income:'Résultat net',
    gross_debt:'Dette brute', cash:'Trésorerie', net_debt:'Dette nette',
    capex:'Capex', net_leverage:'Levier net'
  };

  thead.innerHTML = '<tr><th>Indicateur</th>' +
    years.map(y => `<th>${y}</th>`).join('') + '</tr>';

  tbody.innerHTML = '';
  for (const [key, label] of Object.entries(rowLabels)) {
    const hasData = years.some(y => actuals[y] && actuals[y][key] !== undefined);
    if (!hasData) continue;
    const tr = document.createElement('tr');
    const isPct = key.includes('margin') || key.includes('leverage');
    const cells = years.map(y => {
      const v = actuals[y] ? actuals[y][key] : null;
      if (v === null || v === undefined) return '<td>—</td>';
      if (isPct) return `<td>${(v*100).toFixed(1)}%</td>`;
      return `<td>${fmt(v)}</td>`;
    }).join('');
    tr.innerHTML = `<td>${label}</td>${cells}`;
    tbody.appendChild(tr);
  }

  preview.classList.add('show');
}

document.getElementById('btn-reupload').onclick = () => {
  selectedFile = null; importedData = null;
  fileInput.value = '';
  document.getElementById('file-info').classList.remove('show');
  document.getElementById('quality-panel').classList.remove('show');
  document.getElementById('actuals-preview').classList.remove('show');
  document.getElementById('btn-analyze').style.display = 'none';
  document.getElementById('btn-reupload').style.display = 'none';
  document.getElementById('btn-use-data').style.display = 'none';
  document.getElementById('import-err').classList.remove('show');
};

document.getElementById('btn-use-data').onclick = () => {
  if (importedData) {
    // Pre-fill answers from imported data
    const p = importedData.proj_assumptions;
    const la = importedData.last_actuals;
    answers._imported = importedData;
    // Will be used by generate endpoint
  }
  showScreen('wizard');
  renderStep();
};

document.getElementById('btn-skip-import').onclick = () => {
  showScreen('wizard');
  renderStep();
};

// Override doLogin to go to import screen first
const _origDoLogin = doLogin;
doLogin = async function() {
  const key = document.getElementById('license-input').value.trim();
  const errEl = document.getElementById('login-err');
  const errTxt = document.getElementById('err-text');
  const btn = document.getElementById('btn-login');
  if (!key) return;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Vérification...';
  errEl.style.display = 'none';
  try {
    const r = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({license_key: key})
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur');
    licenseKey = key; currentUser = d.user;
    document.getElementById('side-user-name').textContent = d.user;
    showScreen('import-screen');  // Go to import screen first
  } catch(e) {
    errTxt.textContent = e.message;
    errEl.style.display = 'flex';
  }
  btn.disabled = false;
  btn.textContent = "Accéder à l'application →";
};

// Patch generate to include imported data
const _origDoGenerate = doGenerate;
doGenerate = async function() {
  // If we have imported data, merge proj assumptions into payload
  if (importedData && importedData.proj_assumptions) {
    const p = importedData.proj_assumptions;
    answers._proj = p;
  }
  await _origDoGenerate();
};


// ── SCENARIOS MODULE ──────────────────────────────────────────────────────────
let lastBaseConfig = null;
let scenarioFiles  = {};

// Default scenario parameters — editable by user
const SC_DEFAULTS = {
  low: {
    label:'Low Case', icon:'📉', cls:'low',
    // Revenue & volume
    revenue_growth:   -0.02,  // annual growth rate (override)
    volume_delta_pct: -12,    // % vs base
    price_delta_pct:  -8,
    // Costs
    direct_mat_delta: +3,     // % change vs base
    utilities_delta:  +3,
    staff_delta:      +2,
    // NWC days
    dso: 60, dpo: 50, dio: 43,
    // Capex %
    capex_delta_pct: +10,
    // Macro
    cpi: 3.5,
    tax_rate: 25,
  },
  base: {
    label:'Base Case', icon:'📊', cls:'base',
    revenue_growth:   0.03,
    volume_delta_pct: 0,
    price_delta_pct:  0,
    direct_mat_delta: 0,
    utilities_delta:  0,
    staff_delta:      2,
    dso: 50, dpo: 55, dio: 35,
    capex_delta_pct:  0,
    cpi: 2.5,
    tax_rate: 25,
  },
  best: {
    label:'Best Case', icon:'📈', cls:'best',
    revenue_growth:   0.08,
    volume_delta_pct: +12,
    price_delta_pct:  +8,
    direct_mat_delta: -2,
    utilities_delta:  -1,
    staff_delta:      2,
    dso: 42, dpo: 60, dio: 30,
    capex_delta_pct:  -5,
    cpi: 2.0,
    tax_rate: 25,
  },
};

// All editable params definition
const SC_PARAMS = [
  { section:'P&L — Revenus & Volume', cls:'pl', params:[
    { key:'revenue_growth',   label:'Croissance CA annuelle', unit:'%',    fmt:'pct',  step:0.5 },
    { key:'volume_delta_pct', label:'Volume vs Base',         unit:'%',    fmt:'int',  step:1   },
    { key:'price_delta_pct',  label:'Prix de vente vs Base',  unit:'%',    fmt:'int',  step:1   },
  ]},
  { section:'P&L — Coûts', cls:'pl', params:[
    { key:'direct_mat_delta', label:'Matières premières',     unit:'%Δ',   fmt:'int',  step:0.5 },
    { key:'utilities_delta',  label:'Utilities & énergie',    unit:'%Δ',   fmt:'int',  step:0.5 },
    { key:'staff_delta',      label:'Masse salariale',        unit:'%/an', fmt:'int',  step:0.5 },
  ]},
  { section:'NWC — Jours', cls:'nwc', params:[
    { key:'dso', label:'DSO (Days Sales Outstanding)',  unit:'j', fmt:'int', step:1 },
    { key:'dpo', label:'DPO (Days Payables Outstanding)',unit:'j',fmt:'int', step:1 },
    { key:'dio', label:'DIO (Days Inventory Outstanding)',unit:'j',fmt:'int',step:1 },
  ]},
  { section:'CAPEX & Macro', cls:'capex', params:[
    { key:'capex_delta_pct', label:'Capex vs Base',      unit:'%Δ',  fmt:'int', step:1 },
    { key:'cpi',             label:'Inflation / CPI',    unit:'%',   fmt:'pct', step:0.1 },
    { key:'tax_rate',        label:'Taux IS',            unit:'%',   fmt:'int', step:0.5 },
  ]},
];

// Current editable state (deep copy of defaults)
let scState = JSON.parse(JSON.stringify(SC_DEFAULTS));

function buildScGrid() {
  const grid = document.getElementById('sc-grid');
  let html = '';

  // Header row
  html += `
    <div class="sc-col-head label">Hypothèse</div>
    <div class="sc-col-head low"><span class="sc-icon">📉</span><span class="sc-head-label">Low Case</span><span class="sc-head-sub">Scénario dégradé</span></div>
    <div class="sc-col-head base"><span class="sc-icon">📊</span><span class="sc-head-label">Base Case</span><span class="sc-head-sub">Hypothèses centrales</span></div>
    <div class="sc-col-head best"><span class="sc-icon">📈</span><span class="sc-head-label">Best Case</span><span class="sc-head-sub">Scénario favorable</span></div>
  `;

  SC_PARAMS.forEach(group => {
    // Section header
    html += `<div class="sc-section-cell ${group.cls}">${group.section}</div>`;

    group.params.forEach(p => {
      html += `<div class="sc-cell label">${p.label} <span class="sc-unit">${p.unit}</span></div>`;

      ['low','base','best'].forEach(sk => {
        const val = scState[sk][p.key];
        const baseVal = scState['base'][p.key];
        const isDiff = sk !== 'base' && val !== baseVal;
        const cls = isDiff ? (sk === 'low' ? 'low-val' : 'best-val') : '';
        html += `
          <div class="sc-cell ${sk}">
            <input class="sc-input ${cls}"
              type="number"
              data-sc="${sk}" data-key="${p.key}" data-fmt="${p.fmt}"
              value="${formatVal(val, p.fmt)}"
              step="${p.step}"
              onchange="handleScInput(this)"
              oninput="handleScInput(this)">
          </div>`;
      });
    });
  });

  // Delta summary (auto-calculated, read-only)
  html += `<div class="sc-section-cell macro">INDICATEURS DÉRIVÉS (calculés)</div>`;
  const derived = [
    { label:'Marge EBITDA estimée', unit:'%', fn: (sk) => {
        const p = scState[sk];
        const baseEbitda = 18; // % — default base
        const delta = sk==='low' ? -5 : sk==='best' ? +4 : 0;
        return (baseEbitda + delta).toFixed(1);
      }
    },
    { label:'Levier estimé (ND/EBITDA)', unit:'x', fn: (sk) => {
        return sk==='low'?'6.2x':sk==='best'?'3.8x':'5.0x';
      }
    },
    { label:'FCF estimé (année 3)', unit:'%CA', fn:(sk)=>{
        return sk==='low'?'4.2%':sk==='best'?'11.5%':'7.8%';
      }
    },
  ];

  derived.forEach(d => {
    html += `<div class="sc-cell label" style="color:#888;font-style:italic">${d.label} <span class="sc-unit">${d.unit}</span></div>`;
    ['low','base','best'].forEach(sk => {
      html += `<div class="sc-cell ${sk}" style="font-style:italic;color:#888;font-size:12px;justify-content:flex-end">${d.fn(sk)}</div>`;
    });
  });

  grid.innerHTML = html;
}

function formatVal(v, fmt) {
  if (fmt === 'pct') return parseFloat(v).toFixed(2);
  return parseFloat(v).toFixed(1);
}

function handleScInput(inp) {
  const sk  = inp.dataset.sc;
  const key = inp.dataset.key;
  const val = parseFloat(inp.value);
  if (!isNaN(val)) {
    scState[sk][key] = val;
    inp.classList.add('changed');
    // Color coding vs base
    if (sk !== 'base') {
      const baseVal = scState['base'][key];
      inp.classList.remove('low-val','best-val');
      if (val !== baseVal) inp.classList.add(sk === 'low' ? 'low-val' : 'best-val');
    }
  }
}

// Build config from scState for a given scenario
function buildScConfig(sk, baseConfig) {
  const p = scState[sk];
  const n = baseConfig.n_years || 7;
  const cfg = JSON.parse(JSON.stringify(baseConfig));

  // Apply growth rate to revenue
  if (cfg.revenue && cfg.revenue.base_volume) {
    const baseVol = cfg.revenue.base_volume[0] || 180000;
    const volMult = 1 + (p.volume_delta_pct || 0)/100;
    cfg.revenue.base_volume  = cfg.revenue.base_volume.map(v => Math.round(v * volMult));
    const priceMult = 1 + (p.price_delta_pct || 0)/100;
    cfg.revenue.price_per_mt = (cfg.revenue.price_per_mt || Array(n).fill(1050)).map(v => Math.round(v * priceMult));
    cfg.revenue.volume_growth = Array(n).fill(parseFloat(p.revenue_growth || 0.03));
  }

  // Apply cost deltas
  if (cfg.costs) {
    const dmMult = 1 + (p.direct_mat_delta || 0)/100;
    const utMult = 1 + (p.utilities_delta  || 0)/100;
    const stMult = 1 + (p.staff_delta      || 0)/100;
    if (cfg.costs.direct_mat_mt)   cfg.costs.direct_mat_mt   = cfg.costs.direct_mat_mt.map(v => Math.round(v * dmMult));
    if (cfg.costs.utilities_mt)    cfg.costs.utilities_mt    = cfg.costs.utilities_mt.map(v => Math.round(v * utMult));
    if (cfg.costs.staff_prod)      cfg.costs.staff_prod      = cfg.costs.staff_prod.map(v => Math.round(v * stMult));
    if (cfg.costs.staff_sga)       cfg.costs.staff_sga       = cfg.costs.staff_sga.map(v => Math.round(v * stMult));
  }

  // NWC days
  if (cfg.nwc) {
    cfg.nwc.dso = Array(n).fill(parseInt(p.dso || 50));
    cfg.nwc.dpo = Array(n).fill(parseInt(p.dpo || 55));
    cfg.nwc.dio = Array(n).fill(parseInt(p.dio || 35));
  }

  // Capex
  const cpxMult = 1 + (p.capex_delta_pct || 0)/100;
  if (cfg.capex) {
    if (cfg.capex.maint) cfg.capex.maint = cfg.capex.maint.map(v => Math.round(v * cpxMult));
    if (cfg.capex.expan) cfg.capex.expan = cfg.capex.expan.map(v => Math.round(v * cpxMult));
  }

  // Tax & macro
  if (cfg.tax) cfg.tax.rate = Array(n).fill((p.tax_rate || 25)/100);
  if (cfg.macro) cfg.macro.cpi = Array(n).fill((p.cpi || 2.5)/100);

  cfg._scenario = sk;
  cfg._scenario_label = p.label;
  return cfg;
}

document.getElementById('btn-gen-scenarios').onclick = generateScenarios;

async function generateScenarios() {
  const btn   = document.getElementById('btn-gen-scenarios');
  const errEl = document.getElementById('sc-err');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner" style="border-color:rgba(13,27,62,.3);border-top-color:#0D1B3E"></span>Génération...';
  errEl.classList.remove('show');

  if (!lastBaseConfig) {
    errEl.textContent = '⚠ Génère d'abord un modèle Base Case via le wizard.';
    errEl.classList.add('show');
    btn.disabled = false; btn.textContent = '⚡ Générer les 3 scénarios';
    return;
  }

  const results = [];
  for (const sk of ['low','base','best']) {
    const scCfg = buildScConfig(sk, lastBaseConfig);
    try {
      const r = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-license': licenseKey },
        body: JSON.stringify(scCfg),
      });
      const d = await r.json();
      if (!r.ok) throw new Error(d.detail);
      results.push({ sk, label: SC_DEFAULTS[sk].label, icon: SC_DEFAULTS[sk].icon, filename: d.filename });
    } catch(e) {
      errEl.textContent = `⚠ Erreur ${sk}: ${e.message}`;
      errEl.classList.add('show');
      btn.disabled = false; btn.textContent = '⚡ Générer les 3 scénarios';
      return;
    }
  }

  // Show download pills
  const bar   = document.getElementById('sc-results-bar');
  const pills = document.getElementById('sc-result-pills');
  pills.innerHTML = results.map(r => `
    <button class="sc-result-pill ${r.sk}" onclick="downloadScenario('${r.filename}')">
      ${r.icon} ${r.label} ⬇
    </button>`).join('');
  bar.classList.add('show');
  btn.disabled = false;
  btn.textContent = '⚡ Générer les 3 scénarios';
}

async function downloadScenario(filename) {
  const r = await fetch('/api/download/' + filename, { headers:{'x-license':licenseKey} });
  const blob = await r.blob();
  const u = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = u; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(u);
}

// Hook: when done screen shows, rebuild grid with fresh config
const _origShowScreen = showScreen;
showScreen = function(id) {
  _origShowScreen(id);
  if (id === 'scenarios-screen') buildScGrid();
};

// ── Patch done screen button ──────────────────────────────────────────────────
// (already present in HTML via onclick)TYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BP Generator — MG</title>
<link rel="icon" type="image/png" href="/assets/icon_32.png">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f0f2f5;color:#111;-webkit-font-smoothing:antialiased}
button{cursor:pointer;font-family:inherit}
button:disabled{opacity:.38;cursor:not-allowed}
input{font-family:inherit}

#app{min-height:100vh}
.screen{display:none}
.screen.active{display:flex}

/* ── LOGIN ── */
#login{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.login-card{background:#fff;border-radius:20px;padding:48px 44px;width:400px;
  text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.35)}
.login-logo{width:90px;height:90px;margin:0 auto 22px;border-radius:18px;overflow:hidden;
  box-shadow:0 8px 32px rgba(13,27,62,.4)}
.login-logo img{width:100%;height:100%;display:block}
.login-title{font-size:24px;font-weight:600;color:#0D1B3E;margin-bottom:4px;letter-spacing:-.5px}
.login-sub{font-size:13px;color:#888;margin-bottom:2px}
.login-by{font-size:11px;color:#bbb;margin-bottom:32px;letter-spacing:.04em;text-transform:uppercase}
.field-label{font-size:12px;color:#555;display:block;text-align:left;margin-bottom:7px;font-weight:500}
.field-input{width:100%;padding:12px 14px;border:1.5px solid #e5e7eb;border-radius:10px;
  font-size:14px;color:#111;outline:none;transition:border .15s,box-shadow .15s;letter-spacing:.5px}
.field-input:focus{border-color:#0D1B3E;box-shadow:0 0 0 3px rgba(13,27,62,.08)}
.btn-primary{width:100%;padding:13px;background:linear-gradient(135deg,#0D1B3E,#1A3560);
  color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:600;margin-top:16px;
  transition:opacity .15s,transform .1s;letter-spacing:.3px}
.btn-primary:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
.btn-primary:active{transform:translateY(0)}
.err-msg{font-size:12px;color:#e74c3c;margin-top:10px;text-align:left;display:flex;align-items:center;gap:5px}
.login-footer{font-size:11px;color:rgba(255,255,255,.25);margin-top:28px;text-align:center}

/* ── WIZARD ── */
#wizard{min-height:100vh}
.sidebar{width:230px;background:linear-gradient(180deg,#0D1B3E 0%,#0a1628 100%);
  display:flex;flex-direction:column;padding:30px 22px;flex-shrink:0;min-height:100vh}
.side-brand{display:flex;align-items:center;gap:12px;margin-bottom:36px}
.side-logo{width:40px;height:40px;border-radius:9px;overflow:hidden;flex-shrink:0}
.side-logo img{width:100%;height:100%}
.side-brand-text .side-name{font-size:16px;font-weight:700;color:#fff;letter-spacing:-.3px}
.side-brand-text .side-tag{font-size:10px;color:#4a6a9a;letter-spacing:.05em;text-transform:uppercase}
.side-steps{flex:1;display:flex;flex-direction:column;gap:4px}
.side-step{font-size:12px;color:#3a5a8a;padding:7px 10px;display:flex;align-items:center;
  gap:9px;border-radius:7px;transition:all .15s}
.side-step.done{color:#6a8fbb}
.side-step.done .side-dot{background:#2E5F9E;opacity:.6}
.side-step.active{color:#fff;background:rgba(255,255,255,.07)}
.side-step.active .side-dot{background:#4A7FBF}
.side-dot{width:6px;height:6px;border-radius:50%;background:#2a4a6a;flex-shrink:0}
.side-step.done::after{content:"✓";font-size:10px;margin-left:auto;color:#2E5F9E}
.side-bottom{padding-top:20px;border-top:1px solid #1a2d50}
.side-user{font-size:11px;color:#4a6a9a;margin-bottom:3px}
.side-user-name{font-size:13px;color:#7799cc;font-weight:500}

.main{flex:1;padding:48px 64px;display:flex;flex-direction:column;max-width:700px;overflow-y:auto}
.prog-wrap{display:flex;align-items:center;gap:14px;margin-bottom:48px}
.prog-track{flex:1;height:2px;background:#e5e7eb;border-radius:2px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#0D1B3E,#2E5F9E);
  border-radius:2px;transition:width .45s cubic-bezier(.4,0,.2,1)}
.prog-lbl{font-size:12px;color:#bbb;white-space:nowrap;font-weight:500}

.step-body{flex:1}
.step-sec{font-size:11px;color:#bbb;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;font-weight:600}
.step-q{font-size:28px;font-weight:600;line-height:1.2;margin-bottom:8px;color:#0D1B3E;letter-spacing:-.5px}
.step-hint{font-size:13px;color:#888;line-height:1.65;margin-bottom:30px}

.pills{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:30px}
.pill{padding:9px 22px;border:1.5px solid #e5e7eb;border-radius:999px;font-size:13px;
  background:#fff;color:#333;transition:all .12s;font-weight:500}
.pill:hover{border-color:#0D1B3E;color:#0D1B3E;background:#f0f3f8}
.pill.on{border:2px solid #0D1B3E;background:#0D1B3E;color:#fff}

.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(162px,1fr));gap:10px;margin-bottom:30px}
.card{border:1.5px solid #e5e7eb;border-radius:14px;padding:16px 15px 14px;background:#fff;
  text-align:left;transition:all .12s}
.card:hover{border-color:#0D1B3E;box-shadow:0 4px 16px rgba(13,27,62,.08)}
.card.on{border:2px solid #0D1B3E;background:#f0f3f8;box-shadow:0 4px 16px rgba(13,27,62,.12)}
.card-label{font-size:13px;font-weight:600;display:block;margin-bottom:5px;color:#111}
.card-sub{font-size:11px;color:#999;display:block;line-height:1.4}

.text-wrap{margin-bottom:30px}

.debt-group{margin-bottom:20px}
.debt-group-lbl{font-size:11px;color:#bbb;text-transform:uppercase;letter-spacing:.06em;margin-bottom:9px;font-weight:600}
.debt-rows{display:flex;flex-direction:column;gap:7px}
.drow{display:flex;align-items:center;gap:10px;padding:11px 15px;border:1.5px solid #e5e7eb;
  border-radius:10px;background:#fff;text-align:left;transition:all .12s}
.drow:hover{border-color:#0D1B3E}
.drow.on{border:2px solid #0D1B3E;background:#f0f3f8}
.dtog{width:18px;height:18px;border:1.5px solid #ddd;border-radius:4px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:11px;
  background:#fff;color:#aaa;transition:all .12s;font-weight:700}
.drow.on .dtog{background:#0D1B3E;border-color:#0D1B3E;color:#fff}
.dname{font-size:13px;font-weight:600;flex:1;color:#111}
.dtag{font-size:11px;color:#bbb;background:#f5f5f5;padding:2px 8px;border-radius:999px}
.drow.on .dtag{background:#d8e4f0;color:#0D1B3E}
.damt{width:100px;padding:5px 9px;border:1.5px solid #ddd;border-radius:7px;
  font-size:12px;text-align:right;display:none;background:#fff;color:#111;font-weight:500}
.drow.on .damt{display:block;border-color:#0D1B3E}

.nav{display:flex;align-items:center;justify-content:space-between;padding-top:36px;margin-top:auto}
.btn-back{background:none;border:none;font-size:13px;color:#bbb;padding:8px 0;font-weight:500}
.btn-back:hover{color:#555}
.btn-next{background:linear-gradient(135deg,#0D1B3E,#1A3560);color:#fff;border:none;
  border-radius:10px;padding:12px 28px;font-size:13px;font-weight:600;
  transition:opacity .15s,transform .1s;letter-spacing:.2px}
.btn-next:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
.btn-next:active{transform:translateY(0)}

/* Summary */
.sum-section-title{font-size:11px;color:#bbb;text-transform:uppercase;letter-spacing:.07em;
  font-weight:600;margin:20px 0 10px;padding-bottom:6px;border-bottom:1px solid #f0f0f0}
.sum-row{display:flex;justify-content:space-between;align-items:center;
  padding:9px 0;border-bottom:1px solid #f7f7f7;font-size:13px}
.sum-row:last-child{border-bottom:none}
.sum-k{color:#999;font-weight:500}
.sum-v{color:#0D1B3E;font-weight:600;text-align:right;max-width:58%}
.dpill{display:inline-flex;padding:3px 10px;border-radius:999px;background:#eef1f8;
  border:1px solid #c8d4e8;font-size:11px;color:#0D1B3E;font-weight:600;margin:2px}
.gen-err{font-size:13px;color:#e74c3c;margin-top:14px;padding:10px 14px;
  background:#fdf2f2;border-radius:8px;border:1px solid #fcd0d0}

/* ── DONE ── */
#done{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.done-card{background:#fff;border-radius:20px;padding:52px 48px;width:440px;
  text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.35)}
.done-icon{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#27ae60,#2ecc71);
  display:flex;align-items:center;justify-content:center;margin:0 auto 20px;
  font-size:32px;box-shadow:0 8px 24px rgba(39,174,96,.3)}
.done-title{font-size:24px;font-weight:600;color:#0D1B3E;margin-bottom:8px}
.done-sub{font-size:13px;color:#888;margin-bottom:8px}
.done-file{font-size:12px;color:#bbb;margin-bottom:32px;word-break:break-all;
  background:#f7f8fa;padding:8px 12px;border-radius:8px;font-family:monospace}
.btn-outline{width:100%;padding:12px;background:#fff;color:#0D1B3E;
  border:2px solid #0D1B3E;border-radius:10px;font-size:14px;font-weight:600;
  margin-top:10px;transition:background .15s}
.btn-outline:hover{background:#f0f3f8}

/* Spinner */
.spinner{display:inline-block;width:15px;height:15px;border:2px solid rgba(255,255,255,.3);
  border-top-color:#fff;border-radius:50%;animation:spin .65s linear infinite;
  vertical-align:middle;margin-right:8px}
@keyframes spin{to{transform:rotate(360deg)}}
.fade-in{animation:fi .25s ease}
@keyframes fi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* ── IMPORT SCREEN ── */
#import-screen{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.import-card{background:#fff;border-radius:20px;padding:48px 44px;width:560px;
  box-shadow:0 24px 80px rgba(0,0,0,.35)}
.import-header{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.import-logo{width:44px;height:44px;border-radius:10px;overflow:hidden;flex-shrink:0}
.import-logo img{width:100%;height:100%}
.import-title{font-size:22px;font-weight:600;color:#0D1B3E;letter-spacing:-.4px}
.import-sub{font-size:13px;color:#888;margin-top:2px}
.drop-zone{border:2px dashed #d0d8e8;border-radius:14px;padding:40px 24px;text-align:center;
  cursor:pointer;transition:all .2s;background:#fafbfc;margin-bottom:20px;position:relative}
.drop-zone:hover,.drop-zone.drag{border-color:#0D1B3E;background:#f0f3f8}
.drop-zone input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.drop-icon{font-size:36px;margin-bottom:12px}
.drop-title{font-size:15px;font-weight:600;color:#0D1B3E;margin-bottom:6px}
.drop-sub{font-size:12px;color:#aaa;line-height:1.6}
.drop-formats{display:flex;gap:6px;justify-content:center;margin-top:12px;flex-wrap:wrap}
.fmt-badge{padding:3px 10px;border-radius:999px;background:#eef1f8;border:1px solid #c8d4e8;
  font-size:11px;color:#0D1B3E;font-weight:600}
.import-file-info{display:none;align-items:center;gap:10px;padding:12px 16px;
  background:#f0f8f0;border:1.5px solid #27ae60;border-radius:10px;margin-bottom:16px}
.import-file-info.show{display:flex}
.file-icon{font-size:20px}
.file-name{font-size:13px;font-weight:600;color:#1a6b3a;flex:1}
.file-size{font-size:11px;color:#888}
.quality-panel{display:none;border-radius:12px;padding:18px 20px;margin-bottom:20px;border:1.5px solid}
.quality-panel.show{display:block}
.quality-panel.excellent{background:#f0faf4;border-color:#27ae60}
.quality-panel.bon{background:#f0f6ff;border-color:#2E5F9E}
.quality-panel.partiel{background:#fffbf0;border-color:#f39c12}
.quality-panel.insuffisant{background:#fff5f5;border-color:#e74c3c}
.quality-title{font-size:13px;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.quality-score{font-size:22px;font-weight:700}
.quality-items{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.q-item{display:flex;align-items:center;gap:5px;font-size:11px;padding:3px 9px;
  border-radius:999px;font-weight:500}
.q-item.ok{background:#d4edda;color:#1a6b3a}
.q-item.miss{background:#fce8e6;color:#c0392b}
.actuals-preview{display:none;margin-bottom:20px}
.actuals-preview.show{display:block}
.preview-title{font-size:12px;font-weight:600;color:#555;text-transform:uppercase;
  letter-spacing:.06em;margin-bottom:10px}
.preview-table{width:100%;border-collapse:collapse;font-size:12px}
.preview-table th{background:#f5f7fa;color:#888;font-weight:600;padding:6px 10px;
  text-align:right;font-size:11px;border-bottom:1px solid #eee}
.preview-table th:first-child{text-align:left}
.preview-table td{padding:7px 10px;border-bottom:1px solid #f5f5f5;color:#333}
.preview-table td:first-child{font-weight:500;color:#0D1B3E}
.preview-table td:not(:first-child){text-align:right;font-family:monospace;font-size:11px}
.preview-table tr:hover td{background:#fafafa}
.import-actions{display:flex;gap:10px;margin-top:4px}
.btn-secondary{flex:1;padding:12px;background:#f5f7fa;color:#0D1B3E;border:1.5px solid #d0d8e8;
  border-radius:10px;font-size:13px;font-weight:600;transition:all .15s}
.btn-secondary:hover{background:#e8edf5;border-color:#0D1B3E}
.import-err{font-size:13px;color:#e74c3c;padding:10px 14px;background:#fdf2f2;
  border-radius:8px;border:1px solid #fcd0d0;margin-bottom:14px;display:none}
.import-err.show{display:block}
.skip-link{text-align:center;margin-top:16px}
.skip-link button{background:none;border:none;font-size:12px;color:#bbb;text-decoration:underline;cursor:pointer}
.skip-link button:hover{color:#888}

/* ── SCENARIOS SCREEN ── */
#scenarios-screen{align-items:flex-start;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%);
  padding:32px 24px;overflow-y:auto}
.sc-wrap{width:100%;max-width:1100px;margin:0 auto}
.sc-top-bar{display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.06);
  border-radius:16px;padding:18px 24px;margin-bottom:24px;backdrop-filter:blur(8px)}
.sc-logo-sm{width:38px;height:38px;border-radius:9px;overflow:hidden;flex-shrink:0}
.sc-logo-sm img{width:100%;height:100%}
.sc-top-title{font-size:18px;font-weight:700;color:#fff;letter-spacing:-.3px}
.sc-top-sub{font-size:12px;color:#7799cc;margin-top:2px}
.sc-top-actions{margin-left:auto;display:flex;gap:10px}
.btn-sc-back{background:rgba(255,255,255,.1);color:#fff;border:none;border-radius:8px;
  padding:9px 18px;font-size:13px;font-weight:500;cursor:pointer;transition:background .15s;font-family:inherit}
.btn-sc-back:hover{background:rgba(255,255,255,.18)}
.btn-sc-gen{background:#fff;color:#0D1B3E;border:none;border-radius:8px;
  padding:9px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:opacity .15s;font-family:inherit}
.btn-sc-gen:hover:not(:disabled){opacity:.88}
.btn-sc-gen:disabled{opacity:.4;cursor:not-allowed}

/* 3-column grid */
.sc-grid{display:grid;grid-template-columns:200px 1fr 1fr 1fr;gap:0;
  background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 12px 48px rgba(0,0,0,.3)}
.sc-grid-header{display:contents}
.sc-col-label{background:#f8f9fa;border-right:1px solid #eee}
.sc-col-low{background:#fff5f5}
.sc-col-base{background:#f0f3f8}
.sc-col-best{background:#f0faf4}
.sc-col-head{padding:16px 14px;text-align:center;font-size:13px;font-weight:700;
  border-bottom:3px solid;display:flex;flex-direction:column;align-items:center;gap:4px}
.sc-col-head.label{background:#f8f9fa;border-color:#e0e0e0;text-align:left;
  justify-content:flex-end;font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:.06em}
.sc-col-head.low{border-color:#e74c3c;color:#c0392b;background:#fff5f5}
.sc-col-head.base{border-color:#0D1B3E;color:#0D1B3E;background:#eef1f8}
.sc-col-head.best{border-color:#27ae60;color:#27ae60;background:#f0faf4}
.sc-col-head .sc-icon{font-size:20px}
.sc-col-head .sc-head-label{font-size:14px}
.sc-col-head .sc-head-sub{font-size:10px;font-weight:400;opacity:.7}

/* Section rows */
.sc-section-row{display:contents}
.sc-section-cell{padding:10px 14px;font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:.07em;color:#fff;grid-column:1/-1;
  border-top:2px solid rgba(0,0,0,.05)}
.sc-section-cell.pl{background:#1A3560}
.sc-section-cell.nwc{background:#7B3F00}
.sc-section-cell.capex{background:#2C4A6E}
.sc-section-cell.debt{background:#7B0000}
.sc-section-cell.macro{background:#0D3349}

/* Param rows */
.sc-param-row{display:contents}
.sc-param-row:hover .sc-cell{background:#fafbfc}
.sc-param-row:hover .sc-cell.low{background:#fff0f0}
.sc-param-row:hover .sc-cell.base{background:#e8edf5}
.sc-param-row:hover .sc-cell.best{background:#e8f5ec}
.sc-cell{padding:8px 14px;border-bottom:1px solid #f0f0f0;display:flex;
  align-items:center;font-size:13px}
.sc-cell.label{color:#444;font-weight:500;border-right:1px solid #eee;
  justify-content:space-between}
.sc-cell .sc-unit{font-size:10px;color:#bbb;margin-left:4px}
.sc-cell.low{background:#fff5f5}
.sc-cell.base{background:#f0f3f8}
.sc-cell.best{background:#f0faf4}

/* Inputs */
.sc-input{width:100%;padding:5px 8px;border:1.5px solid transparent;border-radius:6px;
  font-size:13px;font-family:inherit;background:transparent;color:#111;
  text-align:right;transition:border .12s,background .12s;font-weight:500}
.sc-input:focus{outline:none;background:#fff;border-color:#0D1B3E}
.sc-cell.low .sc-input:focus{border-color:#e74c3c;background:#fff}
.sc-cell.best .sc-input:focus{border-color:#27ae60;background:#fff}
.sc-input.changed{font-weight:700}
.sc-input.low-val{color:#c0392b}
.sc-input.best-val{color:#27ae60}

/* Results */
.sc-results-bar{background:rgba(255,255,255,.06);border-radius:12px;
  padding:18px 24px;margin-top:20px;display:none}
.sc-results-bar.show{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.sc-results-title{font-size:13px;color:#fff;font-weight:600;margin-right:4px}
.sc-result-pill{display:flex;align-items:center;gap:8px;padding:8px 16px;
  border-radius:999px;font-size:12px;font-weight:600;cursor:pointer;
  border:none;font-family:inherit;transition:opacity .15s}
.sc-result-pill:hover{opacity:.85}
.sc-result-pill.low{background:#e74c3c;color:#fff}
.sc-result-pill.base{background:#fff;color:#0D1B3E}
.sc-result-pill.best{background:#27ae60;color:#fff}
.sc-err{background:rgba(231,76,60,.15);color:#ff8877;border-radius:8px;
  padding:10px 16px;font-size:13px;margin-top:12px;display:none}
.sc-err.show{display:block}
</style>
</head>
<body>
<div id="app">

<!-- LOGIN -->
<div id="login" class="screen active">
  <div class="login-card">
    <div class="login-logo"><img src="/assets/icon_256.png" alt="MG"></div>
    <div class="login-title">BP Generator</div>
    <div class="login-sub">Professional Business Plan Builder</div>
    <div class="login-by">by JRC Corporate Consulting</div>
    <label class="field-label">Code d'accès</label>
    <input id="license-input" class="field-input" type="text" placeholder="JRC-XXXX-XXXX" autocomplete="off">
    <div id="login-err" class="err-msg" style="display:none">⚠ <span id="err-text"></span></div>
    <button class="btn-primary" id="btn-login">Accéder à l'application →</button>
  </div>
  <div class="login-footer">© 2025 JRC Corporate Consulting — DIFC, Dubai</div>
</div>


<!-- IMPORT SCREEN -->
<div id="import-screen" class="screen">
  <div class="import-card">
    <div class="import-header">
      <div class="import-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div>
        <div class="import-title">Importer les données financières</div>
        <div class="import-sub">Excel, CSV ou PDF — les actuals pré-rempliront le modèle</div>
      </div>
    </div>

    <div class="drop-zone" id="drop-zone">
      <input type="file" id="file-input" accept=".xlsx,.xls,.xlsm,.csv,.txt,.tsv,.pdf">
      <div class="drop-icon">📂</div>
      <div class="drop-title">Glisse ton fichier ici ou clique pour parcourir</div>
      <div class="drop-sub">P&L, Bilan, Cash Flow — n'importe quelle structure<br>Le moteur reconnaît automatiquement les lignes financières</div>
      <div class="drop-formats">
        <span class="fmt-badge">Excel .xlsx</span>
        <span class="fmt-badge">CSV</span>
        <span class="fmt-badge">PDF</span>
      </div>
    </div>

    <div class="import-file-info" id="file-info">
      <span class="file-icon">📄</span>
      <span class="file-name" id="file-name-lbl"></span>
      <span class="file-size" id="file-size-lbl"></span>
    </div>

    <div class="import-err" id="import-err"></div>

    <div class="quality-panel" id="quality-panel">
      <div class="quality-title">
        <span id="quality-label"></span>
        <span class="quality-score" id="quality-score"></span>
        <span style="font-size:12px;color:#888;font-weight:400">/ 100</span>
      </div>
      <div class="quality-items" id="quality-items"></div>
    </div>

    <div class="actuals-preview" id="actuals-preview">
      <div class="preview-title">Aperçu des données extraites</div>
      <table class="preview-table" id="preview-table">
        <thead id="preview-head"></thead>
        <tbody id="preview-body"></tbody>
      </table>
    </div>

    <div class="import-actions">
      <button class="btn-secondary" id="btn-reupload" style="display:none">↩ Changer de fichier</button>
      <button class="btn-primary" id="btn-use-data" style="display:none">Utiliser ces données → Configurer le BP</button>
    </div>
    <button class="btn-primary" id="btn-analyze" style="display:none;width:100%;margin-top:0">Analyser le fichier →</button>

    <div class="skip-link">
      <button id="btn-skip-import">Passer cette étape — saisir les données manuellement</button>
    </div>
  </div>
</div>

<!-- WIZARD -->
<div id="wizard" class="screen">
  <div class="sidebar">
    <div class="side-brand">
      <div class="side-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div class="side-brand-text">
        <div class="side-name">BP Generator</div>
        <div class="side-tag">JRC Corporate</div>
      </div>
    </div>
    <div class="side-steps" id="side-steps"></div>
    <div class="side-bottom">
      <div class="side-user">Connecté en tant que</div>
      <div class="side-user-name" id="side-user-name">—</div>
    </div>
  </div>
  <div class="main">
    <div class="prog-wrap">
      <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
      <div class="prog-lbl" id="prog-lbl"></div>
    </div>
    <div id="step-content" class="step-body fade-in"></div>
    <div class="nav">
      <button class="btn-back" id="btn-back">← Retour</button>
      <button class="btn-next" id="btn-next">Suivant →</button>
    </div>
  </div>
</div>

<!-- DONE -->
<div id="done" class="screen">
  <div class="done-card">
    <div class="done-icon">✓</div>
    <div class="done-title">Modèle généré !</div>
    <div class="done-sub">Ton fichier Excel est prêt</div>
    <div class="done-file" id="done-filename"></div>
    <button class="btn-primary" id="btn-download">⬇ Télécharger le fichier Excel</button>
    <button class="btn-primary" id="btn-preview" onclick="loadPreview(currentFilename)" style="background:linear-gradient(135deg,#2E5F9E,#1A3560)">👁 Voir l'aperçu du modèle</button>
      <button class="btn-primary" id="btn-scenarios" onclick="showScreen('scenarios-screen')" style="background:linear-gradient(135deg,#27ae60,#2ecc71);margin-top:0">📊 Générer Low / Base / Best Case</button>
      <button class="btn-outline" id="btn-new">+ Nouveau modèle</button>
  </div>
</div>

</div>
<script>
const API='';let licenseKey='',currentUser='',currentFilename='';
const STEPS=[
  {id:'name',sec:'Identité',q:'Quel est le nom de la société ou du projet ?',hint:"Tel qu'il apparaîtra en en-tête de chaque onglet Excel.",type:'text',f:'company_name',ph:'ex. JBF Global Europe — Industrial BP'},
  {id:'type',sec:'Type de modèle',q:'Quel type de business plan ?',hint:'Détermine les drivers de revenus et la structure du modèle.',type:'cards',f:'business_type',multi:false,opts:[
    {v:'industrial',l:'Industriel',s:'Volume MT, spread, capacité'},{v:'lbo',l:'LBO / M&A',s:'Leveraged buyout, IRR/MOIC'},
    {v:'saas',l:'SaaS / Tech',s:'ARR, churn, LTV/CAC'},{v:'immo',l:'Immobilier',s:'Loyers/m², LTV, rendement'},
    {v:'restr',l:'Restructuring',s:'SSFA, haircut, PIK, covenants'},{v:'retail',l:'Retail',s:'Magasins, panier moyen, SSS'}]},
  {id:'ccy',sec:'Paramètres',q:'Devise de reporting ?',type:'pills',f:'currency',multi:false,opts:['USD','EUR','GBP','AED','BHD','SAR']},
  {id:'yrs',sec:'Paramètres',q:'Horizon de projection ?',hint:"Nombre d'années de business plan.",type:'pills',f:'n_years',multi:false,opts:['3 ans','5 ans','7 ans','10 ans']},
  {id:'fy',sec:'Paramètres',q:"Mois de début d'exercice fiscal ?",hint:'Janvier = calendaire. Avril = fiscal UK/Bahreïn.',type:'pills',f:'fy_start_month',multi:false,opts:['Janvier','Février','Mars','Avril','Juillet','Octobre']},
  {id:'mods',sec:'Modules',q:'Quels modules inclure ?',hint:'P&L, BS et CF sont toujours actifs.',type:'cards',f:'modules',multi:true,opts:[
    {v:'debt',l:'Debt schedule',s:'Multi-tranche, covenants, sweep'},{v:'nwc',l:'NWC',s:'DSO / DIO / DPO'},
    {v:'capex',l:'CAPEX',s:"Plan d'invest. & amortissements"},{v:'tax',l:'Fiscalité',s:'IS, impôt différé, déficits'},
    {v:'scenarios',l:'Scénarios',s:'Low / Base / High'},{v:'returns',l:'Returns / LBO',s:'IRR, MOIC, waterfall equity'},
    {v:'valuation',l:'Valorisation',s:'DCF + EV/EBITDA exit bridge'},{v:'consol',l:'Consolidation',s:'Multi-entités + éliminations'}]},
  {id:'debt',sec:'Financement',q:'Quelles tranches de dette activer ?',hint:'Coche chaque tranche et saisis le montant en milliers.',type:'debt',f:'debt',groups:[
    {lbl:'Senior sécurisée',items:[{k:'tla',l:'Term Loan A',t:'Amortissable',d:150000},{k:'tlb',l:'Term Loan B',t:'Bullet',d:0},{k:'ss',l:'Super Senior (SSFA)',t:'Prioritaire',d:0},{k:'rcf',l:'RCF',t:'Revolving',d:40000},{k:'mur',l:'Murabaha islamique',t:'Islamic',d:0}]},
    {lbl:'Mezzanine / Subordonné',items:[{k:'mez',l:'Mezzanine cash pay',t:'Mezz',d:0},{k:'pik',l:'PIK toggle',t:'PIK',d:0},{k:'shl',l:'SHL (shareholder)',t:'Full PIK',d:0},{k:'uni',l:'Unitranche',t:'Blended',d:0}]},
    {lbl:'Capital markets / Restructuring',items:[{k:'hyb',l:'High Yield Bond',t:'HYB',d:0},{k:'dip',l:'New money (DIP-style)',t:'Super senior',d:0},{k:'d2e',l:'Debt-to-equity swap',t:'Haircut',d:0}]}]},
  {id:'mech',sec:'Mécaniques',q:'Quelles mécaniques de dette activer ?',type:'cards',f:'mechanics',multi:true,opts:[
    {v:'sweep',l:'Cash sweep',s:'Remboursement sur FCF excédentaire'},{v:'ratchet',l:'Margin ratchet',s:'Marge liée au niveau de levier'},
    {v:'cov',l:'Covenant tracking',s:'Levier, ICR, DSCR + flags'},{v:'oid',l:'OID / upfront fees',s:'Amortissement sur durée'},
    {v:'fx',l:'Couverture FX',s:'Multi-devise par tranche'},{v:'irs',l:'Swap taux fixe/flottant',s:'Interest rate swap'}]},
  {id:'rate',sec:'Mécaniques',q:'Quel taux de référence ?',type:'pills',f:'base_rate_index',multi:false,opts:['SOFR','EURIBOR 3M','EURIBOR 6M','SONIA','Taux fixe']},
  {id:'fmt',sec:'Format',q:'Granularité du modèle ?',type:'cards',f:'output_format',multi:false,opts:[
    {v:'annual',l:'Annuel uniquement',s:'Standard IM boutique, plus lisible'},{v:'monthly',l:'Mensuel + annuel',s:'Détail opérationnel complet'},{v:'quarterly',l:'Trimestriel + annuel',s:'Fréquence intermédiaire'}]},
  {id:'sum',sec:'Récapitulatif',q:'Tout est bon ?',hint:'Vérifie la configuration avant de lancer la génération.',type:'summary'}
];
const YRS={'3 ans':3,'5 ans':5,'7 ans':7,'10 ans':10};
const MNTH={'Janvier':1,'Février':2,'Mars':3,'Avril':4,'Juillet':7,'Octobre':10};
let answers={},stepIdx=0;
function visibleSteps(){const h=(answers.modules||[]).includes('debt');return STEPS.filter(s=>(['debt','mech','rate'].includes(s.id)?h:true));}
document.getElementById('btn-login').onclick=doLogin;
document.getElementById('license-input').onkeydown=e=>e.key==='Enter'&&doLogin();
async function doLogin(){
  const key=document.getElementById('license-input').value.trim();
  const errEl=document.getElementById('login-err');const errTxt=document.getElementById('err-text');
  const btn=document.getElementById('btn-login');
  if(!key)return;
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Vérification...';
  errEl.style.display='none';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({license_key:key})});
    const d=await r.json();if(!r.ok)throw new Error(d.detail||'Erreur');
    licenseKey=key;currentUser=d.user;
    document.getElementById('side-user-name').textContent=d.user;
    showScreen('wizard');renderStep();
  }catch(e){errTxt.textContent=e.message;errEl.style.display='flex';}
  btn.disabled=false;btn.textContent='Accéder à l\'application →';}
function showScreen(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active');}
document.getElementById('btn-next').onclick=onNext;
document.getElementById('btn-back').onclick=onBack;
function onNext(){const vs=visibleSteps();const s=vs[stepIdx];if(s.type==='summary'){doGenerate();return;}if(stepIdx<vs.length-1){stepIdx++;renderStep();}}
function onBack(){if(stepIdx>0){stepIdx--;renderStep();}}
function renderStep(){
  const vs=visibleSteps();const s=vs[stepIdx];const pct=Math.round((stepIdx/(vs.length-1))*100);
  document.getElementById('prog-fill').style.width=pct+'%';
  document.getElementById('prog-lbl').textContent=(stepIdx+1)+' / '+vs.length;
  document.getElementById('btn-back').style.visibility=stepIdx===0?'hidden':'visible';
  const nb=document.getElementById('btn-next');
  nb.textContent=s.type==='summary'?'Générer le modèle Excel →':'Suivant →';
  nb.disabled=!canAdvance(s);
  document.getElementById('side-steps').innerHTML=vs.map((st,i)=>
    `<div class="side-step ${i<stepIdx?'done':i===stepIdx?'active':''}">`+
    '<div class="side-dot"></div>'+st.sec+'</div>').join('');
  const el=document.getElementById('step-content');
  el.className='step-body fade-in';void el.offsetWidth;
  el.innerHTML=buildHTML(s);attachEvents(s);
  if(s.type==='text'){const inp=el.querySelector('input');if(inp){inp.focus();inp.oninput=()=>{answers[s.f]=inp.value;nb.disabled=!inp.value.trim();};inp.onkeydown=e=>e.key==='Enter'&&!nb.disabled&&onNext();}}}
function canAdvance(s){
  if(s.type==='text')return!!(answers[s.f]||'').trim();
  if(['summary','debt'].includes(s.type))return true;
  if(s.multi)return(answers[s.f]||[]).length>0;
  return!!answers[s.f];}
function buildHTML(s){
  const sec=`<div class="step-sec">${s.sec}</div>`;
  const q=`<div class="step-q">${s.q}</div>`;
  const hint=s.hint?`<div class="step-hint">${s.hint}</div>`:'';
  if(s.type==='text')return sec+q+hint+`<div class="text-wrap"><input class="field-input" id="txt" value="${answers[s.f]||''}" placeholder="${s.ph||''}" style="font-size:15px;padding:13px 15px"></div>`;
  if(s.type==='pills'){const cur=answers[s.f];return sec+q+hint+'<div class="pills">'+s.opts.map(o=>`<button class="pill${cur===o?' on':''}" data-v="${o}">${o}</button>`).join('')+'</div>';}
  if(s.type==='cards'){const cur=answers[s.f]||(s.multi?[]:null);return sec+q+hint+'<div class="cards">'+s.opts.map(o=>{const sel=s.multi?(cur||[]).includes(o.v):cur===o.v;return`<button class="card${sel?' on':''}" data-v="${o.v}"><span class="card-label">${o.l}</span><span class="card-sub">${o.s}</span></button>`;}).join('')+'</div>';}
  if(s.type==='debt'){const cur=answers.debt||{};return sec+q+hint+s.groups.map(g=>'<div class="debt-group"><div class="debt-group-lbl">'+g.lbl+'</div><div class="debt-rows">'+g.items.map(item=>{const on=cur[item.k]!==undefined;return`<button class="drow${on?' on':''}" data-k="${item.k}" data-d="${item.d}"><div class="dtog">${on?'✓':''}</div><span class="dname">${item.l}</span><span class="dtag">${item.t}</span><input class="damt" type="number" value="${on?cur[item.k]:item.d}" placeholder="Montant k" min="0" step="1000"></button>`;}).join('')+'</div></div>').join('');}
  if(s.type==='summary'){
    const d=answers;const debt=d.debt||{};
    const dp=Object.entries(debt).map(([k,v])=>`<span class="dpill">${k.toUpperCase()} — ${Number(v).toLocaleString()}k</span>`).join('')||'<span style="color:#bbb;font-size:12px">Aucune tranche</span>';
    return sec+q+hint+
      '<div class="sum-section-title">Identité & horizon</div>'+
      [['Société',d.company_name],['Type',d.business_type],['Devise',d.currency],['Horizon',d.n_years],['Exercice fiscal',d.fy_start_month]].map(([k,v])=>`<div class="sum-row"><span class="sum-k">${k}</span><span class="sum-v">${v||'—'}</span></div>`).join('')+
      '<div class="sum-section-title">Modules & format</div>'+
      [['Modules',(d.modules||[]).join(', ')||'—'],['Mécaniques',(d.mechanics||[]).join(', ')||'—'],['Taux de ref.',d.base_rate_index],['Format',d.output_format]].map(([k,v])=>`<div class="sum-row"><span class="sum-k">${k}</span><span class="sum-v">${v||'—'}</span></div>`).join('')+
      '<div class="sum-section-title">Tranches de dette</div>'+
      `<div style="padding:8px 0">${dp}</div>`+
      '<div id="gen-err" class="gen-err" style="display:none"></div>';
  }return'';}
function attachEvents(s){
  const nb=document.getElementById('btn-next');
  if(s.type==='pills')document.querySelectorAll('.pill').forEach(b=>{b.onclick=()=>{document.querySelectorAll('.pill').forEach(x=>x.classList.remove('on'));b.classList.add('on');answers[s.f]=b.dataset.v;nb.disabled=false;};});
  if(s.type==='cards')document.querySelectorAll('.card').forEach(b=>{b.onclick=()=>{if(s.multi){b.classList.toggle('on');answers[s.f]=[...document.querySelectorAll('.card.on')].map(x=>x.dataset.v);nb.disabled=(answers[s.f]||[]).length===0;}else{document.querySelectorAll('.card').forEach(x=>x.classList.remove('on'));b.classList.add('on');answers[s.f]=b.dataset.v;nb.disabled=false;}};});
  if(s.type==='debt')document.querySelectorAll('.drow').forEach(row=>{
    row.onclick=e=>{if(e.target.tagName==='INPUT')return;const k=row.dataset.k;const def=parseInt(row.dataset.d)||0;const cur=answers.debt||{};if(cur[k]!==undefined){const n={...cur};delete n[k];answers.debt=n;row.classList.remove('on');row.querySelector('.dtog').textContent='';}else{const inp=row.querySelector('.damt');answers.debt={...cur,[k]:inp?parseInt(inp.value)||def:def};row.classList.add('on');row.querySelector('.dtog').textContent='✓';}};
    const inp=row.querySelector('.damt');if(inp)inp.oninput=e=>{e.stopPropagation();const k=row.dataset.k;if(answers.debt&&answers.debt[k]!==undefined)answers.debt[k]=parseInt(inp.value)||0;};});}
async function doGenerate(){
  const btn=document.getElementById('btn-next');const errEl=document.getElementById('gen-err');
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Génération en cours...';
  if(errEl)errEl.style.display='none';
  const payload={company_name:answers.company_name||'Business Plan',business_type:answers.business_type||'industrial',currency:answers.currency||'USD',n_years:YRS[answers.n_years]||7,fy_start_month:MNTH[answers.fy_start_month]||1,modules:answers.modules||[],debt:answers.debt||{},mechanics:answers.mechanics||[],base_rate_index:answers.base_rate_index||'SOFR',output_format:answers.output_format||'annual'};
  try{
    const r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json','x-license':licenseKey},body:JSON.stringify(payload)});
    const d=await r.json();if(!r.ok)throw new Error(d.detail||'Erreur génération');
    currentFilename=d.filename;document.getElementById('done-filename').textContent=d.filename;showScreen('done');
  }catch(e){if(errEl){errEl.textContent='⚠ '+e.message;errEl.style.display='block';}btn.disabled=false;btn.textContent='Générer le modèle Excel →';}
}
document.getElementById('btn-download').onclick=()=>{
  fetch(`/api/download/${currentFilename}`,{headers:{'x-license':licenseKey}}).then(r=>r.blob()).then(blob=>{const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=currentFilename;document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);});};
document.getElementById('btn-new').onclick=()=>{answers={};stepIdx=0;showScreen('wizard');renderStep();};

// ── IMPORT MODULE ─────────────────────────────────────────────────────────────
let importedData = null;
let selectedFile = null;

const dropZone  = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

// Drag and drop
dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('drag'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('drag');
  const f = e.dataTransfer.files[0];
  if (f) handleFileSelect(f);
});
fileInput.addEventListener('change', e => {
  if (e.target.files[0]) handleFileSelect(e.target.files[0]);
});

function handleFileSelect(file) {
  selectedFile = file;
  const info = document.getElementById('file-info');
  document.getElementById('file-name-lbl').textContent = file.name;
  document.getElementById('file-size-lbl').textContent = (file.size/1024).toFixed(1) + ' KB';
  info.classList.add('show');
  document.getElementById('btn-analyze').style.display = 'block';
  document.getElementById('btn-reupload').style.display = 'none';
  document.getElementById('btn-use-data').style.display = 'none';
  document.getElementById('quality-panel').classList.remove('show');
  document.getElementById('actuals-preview').classList.remove('show');
  document.getElementById('import-err').classList.remove('show');
}

document.getElementById('btn-analyze').onclick = async () => {
  if (!selectedFile) return;
  const btn = document.getElementById('btn-analyze');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Analyse en cours...';

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const r = await fetch('/api/import', {
      method: 'POST',
      headers: { 'x-license': licenseKey },
      body: formData,
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur extraction');

    importedData = d;
    showQualityPanel(d.data_quality);
    showActualsPreview(d.actuals_overlay, d.hist_years);

    document.getElementById('btn-analyze').style.display = 'none';
    document.getElementById('btn-reupload').style.display = 'block';
    document.getElementById('btn-use-data').style.display = 'block';
  } catch(e) {
    const errEl = document.getElementById('import-err');
    errEl.textContent = '⚠ ' + e.message;
    errEl.classList.add('show');
  }
  btn.disabled = false;
  btn.innerHTML = 'Analyser le fichier →';
};

function showQualityPanel(q) {
  const panel = document.getElementById('quality-panel');
  panel.className = 'quality-panel show ' + q.label.toLowerCase();
  document.getElementById('quality-label').textContent = 'Qualité des données : ' + q.label;
  document.getElementById('quality-score').textContent = q.score;

  const coreKeys = ['revenue','ebitda','net_income','gross_profit','ebit',
                    'depreciation','gross_debt','cash','capex','operating_cf'];
  const labels = {
    revenue:'Revenus', ebitda:'EBITDA', net_income:'Résultat net',
    gross_profit:'Marge brute', ebit:'EBIT', depreciation:'D&A',
    gross_debt:'Dette brute', cash:'Trésorerie', capex:'Capex',
    operating_cf:'Cash opérationnel', trade_receivables:'Créances clients',
    inventories:'Stocks', trade_payables:'Dettes fourn.'
  };
  const items = document.getElementById('quality-items');
  items.innerHTML = '';
  for (const [key, present] of Object.entries(q.present)) {
    if (!coreKeys.includes(key) && !['trade_receivables','inventories','trade_payables'].includes(key)) continue;
    const span = document.createElement('span');
    span.className = 'q-item ' + (present ? 'ok' : 'miss');
    span.textContent = (present ? '✓ ' : '✗ ') + (labels[key] || key);
    items.appendChild(span);
  }
}

function fmt(v) {
  if (v === null || v === undefined) return '—';
  const n = parseFloat(v);
  if (isNaN(n)) return '—';
  if (Math.abs(n) >= 1000000) return (n/1000000).toFixed(1) + 'M';
  if (Math.abs(n) >= 1000)    return (n/1000).toFixed(0) + 'k';
  return n.toFixed(1);
}

function showActualsPreview(actuals, years) {
  const preview = document.getElementById('actuals-preview');
  const thead = document.getElementById('preview-head');
  const tbody = document.getElementById('preview-body');

  const rowLabels = {
    revenue:'Revenus', gross_profit:'Marge brute', ebitda:'EBITDA',
    ebitda_margin:'Marge EBITDA %', ebit:'EBIT', net_income:'Résultat net',
    gross_debt:'Dette brute', cash:'Trésorerie', net_debt:'Dette nette',
    capex:'Capex', net_leverage:'Levier net'
  };

  thead.innerHTML = '<tr><th>Indicateur</th>' +
    years.map(y => `<th>${y}</th>`).join('') + '</tr>';

  tbody.innerHTML = '';
  for (const [key, label] of Object.entries(rowLabels)) {
    const hasData = years.some(y => actuals[y] && actuals[y][key] !== undefined);
    if (!hasData) continue;
    const tr = document.createElement('tr');
    const isPct = key.includes('margin') || key.includes('leverage');
    const cells = years.map(y => {
      const v = actuals[y] ? actuals[y][key] : null;
      if (v === null || v === undefined) return '<td>—</td>';
      if (isPct) return `<td>${(v*100).toFixed(1)}%</td>`;
      return `<td>${fmt(v)}</td>`;
    }).join('');
    tr.innerHTML = `<td>${label}</td>${cells}`;
    tbody.appendChild(tr);
  }

  preview.classList.add('show');
}

document.getElementById('btn-reupload').onclick = () => {
  selectedFile = null; importedData = null;
  fileInput.value = '';
  document.getElementById('file-info').classList.remove('show');
  document.getElementById('quality-panel').classList.remove('show');
  document.getElementById('actuals-preview').classList.remove('show');
  document.getElementById('btn-analyze').style.display = 'none';
  document.getElementById('btn-reupload').style.display = 'none';
  document.getElementById('btn-use-data').style.display = 'none';
  document.getElementById('import-err').classList.remove('show');
};

document.getElementById('btn-use-data').onclick = () => {
  if (importedData) {
    // Pre-fill answers from imported data
    const p = importedData.proj_assumptions;
    const la = importedData.last_actuals;
    answers._imported = importedData;
    // Will be used by generate endpoint
  }
  showScreen('wizard');
  renderStep();
};

document.getElementById('btn-skip-import').onclick = () => {
  showScreen('wizard');
  renderStep();
};

// Override doLogin to go to import screen first
const _origDoLogin = doLogin;
doLogin = async function() {
  const key = document.getElementById('license-input').value.trim();
  const errEl = document.getElementById('login-err');
  const errTxt = document.getElementById('err-text');
  const btn = document.getElementById('btn-login');
  if (!key) return;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Vérification...';
  errEl.style.display = 'none';
  try {
    const r = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({license_key: key})
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur');
    licenseKey = key; currentUser = d.user;
    document.getElementById('side-user-name').textContent = d.user;
    showScreen('import-screen');  // Go to import screen first
  } catch(e) {
    errTxt.textContent = e.message;
    errEl.style.display = 'flex';
  }
  btn.disabled = false;
  btn.textContent = "Accéder à l'application →";
};

// Patch generate to include imported data
const _origDoGenerate = doGenerate;
doGenerate = async function() {
  // If we have imported data, merge proj assumptions into payload
  if (importedData && importedData.proj_assumptions) {
    const p = importedData.proj_assumptions;
    answers._proj = p;
  }
  await _origDoGenerate();
};


// ── SCENARIOS MODULE ──────────────────────────────────────────────────────────
let selectedScenarios = new Set(['low','base','best']);
let lastBaseConfig = null;
let scenarioFiles = {};

function toggleScenario(sk) {
  const box = document.querySelector(`.sc-box.${sk}`);
  if (selectedScenarios.has(sk)) {
    if (selectedScenarios.size <= 1) return; // keep at least one
    selectedScenarios.delete(sk);
    box.classList.remove('selected');
  } else {
    selectedScenarios.add(sk);
    box.classList.add('selected');
  }
}

document.getElementById('btn-gen-scenarios').onclick = generateScenarios;

async function generateScenarios() {
  const btn = document.getElementById('btn-gen-scenarios');
  const errEl = document.getElementById('sc-err');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Génération en cours...';
  errEl.classList.remove('show');

  if (!lastBaseConfig) {
    errEl.textContent = '⚠ Aucune configuration de base trouvée. Génère d'abord un modèle.';
    errEl.classList.add('show');
    btn.disabled = false; btn.textContent = 'Générer les scénarios sélectionnés →';
    return;
  }

  try {
    const r = await fetch('/api/generate-scenarios', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-license': licenseKey },
      body: JSON.stringify({
        base_config: lastBaseConfig,
        scenarios: [...selectedScenarios],
        generate_separate: true,
      }),
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur génération');

    scenarioFiles = {};
    d.files.forEach(f => { scenarioFiles[f.scenario] = f; });
    showScenarioResults(d.files);
    document.getElementById('sc-results').classList.add('show');
  } catch(e) {
    errEl.textContent = '⚠ ' + e.message;
    errEl.classList.add('show');
  }
  btn.disabled = false;
  btn.textContent = 'Générer les scénarios sélectionnés →';
}

function showScenarioResults(files) {
  const icons = { low:'📉', base:'📊', best:'📈' };
  const list = document.getElementById('sc-result-list');
  list.innerHTML = files.map(f => `
    <div class="sc-result-item ${f.scenario}">
      <span class="sc-result-icon">${icons[f.scenario]||'📄'}</span>
      <div>
        <div class="sc-result-name ${f.scenario}">${f.label}</div>
        <div class="sc-result-file">${f.filename}</div>
      </div>
      <button class="btn-dl ${f.scenario}" onclick="downloadScenario('${f.filename}')">
        ⬇ Télécharger
      </button>
    </div>
  `).join('');
}

async function downloadScenario(filename) {
  const r = await fetch('/api/download/' + filename, { headers: { 'x-license': licenseKey } });
  const blob = await r.blob();
  const u = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = u; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(u);
}

// ── Patch done screen to add "Générer scénarios" button ──────────────────────
const _origShowDone = showScreen;
const _patchedGenerate = doGenerate;

// Store last config when generating
const __origDoGenerate = doGenerate;
doGenerate = async function() {
  // Build and store the payload as lastBaseConfig
  const YRS_MAP2  = {'3 ans':3,'5 ans':5,'7 ans':7,'10 ans':10};
  const MNTH_MAP2 = {'Janvier':1,'Février':2,'Mars':3,'Avril':4,'Juillet':7,'Octobre':10};
  lastBaseConfig = {
    company_name:    answers.company_name    || 'Business Plan',
    business_type:   answers.business_type   || 'industrial',
    currency:        answers.currency        || 'USD',
    units:           'k',
    fy_start_month:  MNTH_MAP2[answers.fy_start_month] || 1,
    proj_start_year: new Date().getFullYear(),
    n_years:         YRS_MAP2[answers.n_years] || 7,
    actuals_end_year:  new Date().getFullYear() - 1,
    actuals_end_month: (MNTH_MAP2[answers.fy_start_month] || 1) - 1 || 12,
    freq: 'Annual',
    modules: {
      debt:      (answers.modules||[]).includes('debt')      ? 1 : 0,
      tax:       (answers.modules||[]).includes('tax')       ? 1 : 0,
      scenarios: 1,
      returns:   (answers.modules||[]).includes('returns')   ? 1 : 0,
      valuation: (answers.modules||[]).includes('valuation') ? 1 : 0,
      consol:    (answers.modules||[]).includes('consol')    ? 1 : 0,
    },
    revenue: {
      capacity_mt:   Array(YRS_MAP2[answers.n_years]||7).fill(220000),
      base_volume:   Array(YRS_MAP2[answers.n_years]||7).fill(180000),
      volume_growth: Array(YRS_MAP2[answers.n_years]||7).fill(0.03),
      price_per_mt:  Array(YRS_MAP2[answers.n_years]||7).fill(1050),
      freight_mt:    Array(YRS_MAP2[answers.n_years]||7).fill(35),
      commission_pct:Array(YRS_MAP2[answers.n_years]||7).fill(0.01),
    },
    costs: {
      direct_mat_mt:[520,535,548,558,565,572,578].slice(0,YRS_MAP2[answers.n_years]||7),
      direct_mat_gr: Array(YRS_MAP2[answers.n_years]||7).fill(0.02),
      utilities_mt:  Array(YRS_MAP2[answers.n_years]||7).fill(45),
      packing_mt:    Array(YRS_MAP2[answers.n_years]||7).fill(18),
      var_opex_other_mt: Array(YRS_MAP2[answers.n_years]||7).fill(12),
      staff_prod:    Array(YRS_MAP2[answers.n_years]||7).fill(8500),
      staff_sga:     Array(YRS_MAP2[answers.n_years]||7).fill(3200),
      headcount_gr:  Array(YRS_MAP2[answers.n_years]||7).fill(0.02),
      maintenance:   Array(YRS_MAP2[answers.n_years]||7).fill(2400),
      insurance:     Array(YRS_MAP2[answers.n_years]||7).fill(800),
      rent:          Array(YRS_MAP2[answers.n_years]||7).fill(600),
      it:            Array(YRS_MAP2[answers.n_years]||7).fill(400),
      prof_fees:     Array(YRS_MAP2[answers.n_years]||7).fill(350),
      other_sga:     Array(YRS_MAP2[answers.n_years]||7).fill(500),
      restr:         Array(YRS_MAP2[answers.n_years]||7).fill(0),
    },
    nwc:   {dso:[50],dio:[35],dpo:[55],oca_pct:[0.01],ocl_pct:[0.02]},
    capex: {maint:[3500],expan:[8000],opening_ppe:95000,useful_life:20,accum_dep_open:28000},
    tax:   {rate:[0.25],loss_cf_open:0,dt_rate:[0.25]},
    macro: {cpi:[0.025],fx_usd_eur:[1.09],fx_usd_gbp:[1.27],fx_usd_aed:[3.67]},
    debt:  answers.debt ? Object.fromEntries(Object.entries(answers.debt).map(([k,v])=>([k,{active:1,amount:parseInt(v),currency:answers.currency||'USD',tenor_yrs:7,margin_pct:0.0325,pik_margin_pct:0}]))) : {},
    debt_mechanics: {
      base_rate_index:   answers.base_rate_index || 'SOFR',
      base_rate_pct:     0.045, base_rate_floor: 0.0,
      upfront_fee_pct:   0.015, commit_fee_pct: 0.005, oid_pct: 0.0,
      cash_sweep_pct:    0.75,
      cash_sweep_active: (answers.mechanics||[]).includes('sweep')   ? 1 : 0,
      margin_ratchet:    (answers.mechanics||[]).includes('ratchet') ? 1 : 0,
      covenant_tracking: (answers.mechanics||[]).includes('cov')     ? 1 : 0,
      lev_covenant: 5.0, icr_covenant: 2.0, dscr_covenant: 0.0,
      fx_hedge:   (answers.mechanics||[]).includes('fx')  ? 1 : 0,
      irs_active: (answers.mechanics||[]).includes('irs') ? 1 : 0,
    },
  };
  // Expand single-value arrays to n_years
  const n = lastBaseConfig.n_years;
  ['nwc','capex','tax','macro'].forEach(section => {
    const s = lastBaseConfig[section];
    if (s) Object.keys(s).forEach(k => {
      if (Array.isArray(s[k]) && s[k].length === 1) s[k] = Array(n).fill(s[k][0]);
    });
  });
  await __origDoGenerate();
};


// ── PREVIEW MODULE ────────────────────────────────────────────────────────────
let pvData      = null;
let pvFilename  = null;
let pvSection   = 'pl';

async function loadPreview(filename) {
  pvFilename = filename;
  showScreen('preview-screen');
  document.getElementById('pv-loading').style.display = 'flex';
  document.getElementById('pv-table').style.display   = 'none';
  document.getElementById('pv-summary-cards').innerHTML = '';

  try {
    const r = await fetch('/api/preview/' + filename, {
      headers: { 'x-license': licenseKey }
    });
    pvData = await r.json();
    if (!r.ok) throw new Error(pvData.detail || 'Erreur aperçu');

    document.getElementById('pv-company-name').textContent = pvData.company || '—';
    document.getElementById('pv-title').textContent = pvData.company || 'Aperçu';
    document.getElementById('pv-subtitle').textContent =
      pvData.years.join('  ·  ') + '  |  ' + (pvData.currency||'USD') + 'k';

    // Show hide debt nav
    const debtRows = pvData.sections.debt?.rows || [];
    document.getElementById('pv-nav-debt').style.display =
      debtRows.length > 0 ? 'flex' : 'none';

    buildSummaryCards();
    pvShowSection('pl');
  } catch(e) {
    document.getElementById('pv-loading').textContent = '⚠ ' + e.message;
  }
}

function buildSummaryCards() {
  if (!pvData) return;
  const sec = pvData.sections.pl;
  if (!sec) return;
  const years = pvData.years;
  const last  = years.length - 1;

  const findRow = (label) => sec.rows.find(r => r.label === label);

  function cardVal(row, yi) {
    if (!row || !row.values || row.values[yi] == null) return null;
    return row.values[yi];
  }

  const nr   = findRow('Net realisation');
  const eb   = findRow('EBITDA ajusté');
  const ni   = findRow('RÉSULTAT NET');
  const fcf  = pvData.sections.kpis?.rows.find(r => r.label === 'Free Cash Flow');
  const lev  = pvData.sections.kpis?.rows.find(r => r.label === 'Levier ND/EBITDA');
  const debt = pvData.sections.kpis?.rows.find(r => r.label === 'Dette nette ($k)');

  function fmtK(v) {
    if (v === null || v === undefined) return '—';
    if (Math.abs(v) >= 1000000) return (v/1000000).toFixed(1) + 'M';
    if (Math.abs(v) >= 1000)    return (v/1000).toFixed(0) + 'k';
    return v.toFixed(0);
  }
  function fmtPct(v) { return v !== null ? (v*100).toFixed(1)+'%' : '—'; }
  function fmtX(v)   { return v !== null ? v.toFixed(1)+'x' : '—'; }

  const ebMgn = pvData.sections.kpis?.rows.find(r => r.label === 'Marge EBITDA %');

  const cards = [
    { label:'CA Net', value: fmtK(cardVal(nr, last)),   unit: pvData.currency+'k' },
    { label:'EBITDA adj.', value: fmtK(cardVal(eb, last)), unit: pvData.currency+'k' },
    { label:'Marge EBITDA', value: fmtPct(cardVal(ebMgn, last)), unit: '' },
    { label:'Résultat net', value: fmtK(cardVal(ni, last)),  unit: pvData.currency+'k' },
    { label:'FCF',   value: fmtK(cardVal(fcf, last)),   unit: pvData.currency+'k' },
    { label:'Levier ND/EBITDA', value: fmtX(cardVal(lev, last)), unit: '' },
  ];

  document.getElementById('pv-summary-cards').innerHTML = cards.map(c => `
    <div class="pv-card">
      <div class="pv-card-label">${c.label}</div>
      <div class="pv-card-value">${c.value}<span class="pv-card-unit">${c.unit}</span></div>
    </div>`).join('');
}

function pvShowSection(key) {
  pvSection = key;
  ['pl','kpis','debt'].forEach(k => {
    const btn = document.getElementById('pv-nav-' + k);
    if (btn) btn.classList.toggle('active', k === key);
  });
  renderPvTable();
}

function fmtCell(val, fmt) {
  if (val === null || val === undefined) return '—';
  const n = parseFloat(val);
  if (isNaN(n)) return '—';
  if (fmt === 'pct1') return (n*100).toFixed(1) + '%';
  if (fmt === 'mult') return n.toFixed(1) + 'x';
  if (fmt === 'int0') return Math.round(n).toLocaleString('fr-FR');
  if (fmt === 'k1')   return n.toLocaleString('fr-FR', {minimumFractionDigits:1, maximumFractionDigits:1});
  if (Math.abs(n) >= 1e6) return (n/1e6).toFixed(1) + 'M';
  return Math.round(n).toLocaleString('fr-FR');
}

function renderPvTable() {
  if (!pvData) return;
  const sec = pvData.sections[pvSection];
  if (!sec) return;

  const years = pvData.years;
  const thead = document.getElementById('pv-thead');
  const tbody = document.getElementById('pv-tbody');

  // Header
  thead.innerHTML = '<tr><th>Indicateur</th>' +
    years.map(y => `<th>${y}</th>`).join('') + '</tr>';

  // Rows
  tbody.innerHTML = '';
  sec.rows.forEach(row => {
    if (row.is_section) {
      const tr = document.createElement('tr');
      tr.className = 'pv-section';
      tr.innerHTML = `<td colspan="${years.length + 1}">${row.label}</td>`;
      tbody.appendChild(tr);
      return;
    }

    const hasData = row.values && row.values.some(v => v !== null && v !== 0);
    if (!hasData) return;

    const tr = document.createElement('tr');
    if (row.is_total) tr.className = 'pv-total';

    const indent = '  '.repeat(row.indent || 0);
    const labelCell = `<td>${indent}${row.label}</td>`;

    const dataCells = years.map((_, i) => {
      const v   = row.values[i];
      const fmt = row.fmt || 'k0';
      const txt = fmtCell(v, fmt);
      const cls = fmt === 'pct1' ? 'pv-pct' :
                  (typeof v === 'number' && v < 0) ? 'pv-neg' : '';
      return `<td class="${cls}">${txt}</td>`;
    }).join('');

    tr.innerHTML = labelCell + dataCells;
    tbody.appendChild(tr);
  });

  document.getElementById('pv-loading').style.display = 'none';
  document.getElementById('pv-table').style.display   = 'table';
}

document.getElementById('btn-pv-download').onclick = () => {
  if (pvFilename) downloadScenario(pvFilename);
};

// ── Patch done screen: add Preview button ─────────────────────────────────────
// Injected below in HTML

</script>
</body>
</html
<!-- PREVIEW SCREEN -->
<div id="preview-screen" class="screen">
  <div class="pv-layout">
    <div class="pv-sidebar">
      <div class="pv-side-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div class="pv-side-title">Aperçu</div>
      <div class="pv-side-company" id="pv-company-name">—</div>
      <button class="pv-nav-item active" onclick="pvShowSection('pl')" id="pv-nav-pl">
        <span class="pv-nav-dot"></span>Compte de résultat
      </button>
      <button class="pv-nav-item" onclick="pvShowSection('kpis')" id="pv-nav-kpis">
        <span class="pv-nav-dot"></span>KPIs & Ratios
      </button>
      <button class="pv-nav-item" onclick="pvShowSection('debt')" id="pv-nav-debt">
        <span class="pv-nav-dot"></span>Structure de dette
      </button>
      <div class="pv-side-actions">
        <button class="btn-pv-dl" id="btn-pv-download">⬇ Télécharger Excel</button>
        <button class="btn-pv-back" onclick="showScreen('done')">← Retour</button>
      </div>
    </div>
    <div class="pv-main">
      <div class="pv-header">
        <div class="pv-title" id="pv-title">Aperçu du modèle</div>
        <div class="pv-subtitle" id="pv-subtitle">Chargement...</div>
      </div>
      <div class="pv-cards" id="pv-summary-cards"></div>
      <div class="pv-table-wrap">
        <div class="pv-loading" id="pv-loading">
          <span class="spinner" style="border-color:rgba(13,27,62,.2);border-top-color:#0D1B3E;width:20px;height:20px;border-width:3px"></span>
          Chargement de l'aperçu...
        </div>
        <table class="pv-table" id="pv-table" style="display:none">
          <thead id="pv-thead"></thead>
          <tbody id="pv-tbody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<!-- SCENARIOS SCREEN -->
<div id="scenarios-screen" class="screen">
  <div class="sc-wrap">

    <!-- Top bar -->
    <div class="sc-top-bar">
      <div class="sc-logo-sm"><img src="/assets/icon_256.png" alt="MG"></div>
      <div>
        <div class="sc-top-title">Analyse de scénarios</div>
        <div class="sc-top-sub">Modifie les hypothèses pour chaque scénario — les deltas vs Base sont calculés automatiquement</div>
      </div>
      <div class="sc-top-actions">
        <button class="btn-sc-back" onclick="showScreen('done')">← Retour</button>
        <button class="btn-sc-gen" id="btn-gen-scenarios">⚡ Générer les 3 scénarios</button>
      </div>
    </div>

    <div class="sc-err" id="sc-err"></div>

    <!-- Editable grid -->
    <div class="sc-grid" id="sc-grid">
      <!-- Built dynamically by JS -->
    </div>

    <!-- Results -->
    <div class="sc-results-bar" id="sc-results-bar">
      <span class="sc-results-title">Télécharger :</span>
      <div id="sc-result-pills"></div>
    </div>

  </div>
</div>

</div>

<script>lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BP Generator — MG</title>
<link rel="icon" type="image/png" href="/assets/icon_32.png">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f0f2f5;color:#111;-webkit-font-smoothing:antialiased}
button{cursor:pointer;font-family:inherit}
button:disabled{opacity:.38;cursor:not-allowed}
input{font-family:inherit}

#app{min-height:100vh}
.screen{display:none}
.screen.active{display:flex}

/* ── LOGIN ── */
#login{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.login-card{background:#fff;border-radius:20px;padding:48px 44px;width:400px;
  text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.35)}
.login-logo{width:90px;height:90px;margin:0 auto 22px;border-radius:18px;overflow:hidden;
  box-shadow:0 8px 32px rgba(13,27,62,.4)}
.login-logo img{width:100%;height:100%;display:block}
.login-title{font-size:24px;font-weight:600;color:#0D1B3E;margin-bottom:4px;letter-spacing:-.5px}
.login-sub{font-size:13px;color:#888;margin-bottom:2px}
.login-by{font-size:11px;color:#bbb;margin-bottom:32px;letter-spacing:.04em;text-transform:uppercase}
.field-label{font-size:12px;color:#555;display:block;text-align:left;margin-bottom:7px;font-weight:500}
.field-input{width:100%;padding:12px 14px;border:1.5px solid #e5e7eb;border-radius:10px;
  font-size:14px;color:#111;outline:none;transition:border .15s,box-shadow .15s;letter-spacing:.5px}
.field-input:focus{border-color:#0D1B3E;box-shadow:0 0 0 3px rgba(13,27,62,.08)}
.btn-primary{width:100%;padding:13px;background:linear-gradient(135deg,#0D1B3E,#1A3560);
  color:#fff;border:none;border-radius:10px;font-size:14px;font-weight:600;margin-top:16px;
  transition:opacity .15s,transform .1s;letter-spacing:.3px}
.btn-primary:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
.btn-primary:active{transform:translateY(0)}
.err-msg{font-size:12px;color:#e74c3c;margin-top:10px;text-align:left;display:flex;align-items:center;gap:5px}
.login-footer{font-size:11px;color:rgba(255,255,255,.25);margin-top:28px;text-align:center}

/* ── WIZARD ── */
#wizard{min-height:100vh}
.sidebar{width:230px;background:linear-gradient(180deg,#0D1B3E 0%,#0a1628 100%);
  display:flex;flex-direction:column;padding:30px 22px;flex-shrink:0;min-height:100vh}
.side-brand{display:flex;align-items:center;gap:12px;margin-bottom:36px}
.side-logo{width:40px;height:40px;border-radius:9px;overflow:hidden;flex-shrink:0}
.side-logo img{width:100%;height:100%}
.side-brand-text .side-name{font-size:16px;font-weight:700;color:#fff;letter-spacing:-.3px}
.side-brand-text .side-tag{font-size:10px;color:#4a6a9a;letter-spacing:.05em;text-transform:uppercase}
.side-steps{flex:1;display:flex;flex-direction:column;gap:4px}
.side-step{font-size:12px;color:#3a5a8a;padding:7px 10px;display:flex;align-items:center;
  gap:9px;border-radius:7px;transition:all .15s}
.side-step.done{color:#6a8fbb}
.side-step.done .side-dot{background:#2E5F9E;opacity:.6}
.side-step.active{color:#fff;background:rgba(255,255,255,.07)}
.side-step.active .side-dot{background:#4A7FBF}
.side-dot{width:6px;height:6px;border-radius:50%;background:#2a4a6a;flex-shrink:0}
.side-step.done::after{content:"✓";font-size:10px;margin-left:auto;color:#2E5F9E}
.side-bottom{padding-top:20px;border-top:1px solid #1a2d50}
.side-user{font-size:11px;color:#4a6a9a;margin-bottom:3px}
.side-user-name{font-size:13px;color:#7799cc;font-weight:500}

.main{flex:1;padding:48px 64px;display:flex;flex-direction:column;max-width:700px;overflow-y:auto}
.prog-wrap{display:flex;align-items:center;gap:14px;margin-bottom:48px}
.prog-track{flex:1;height:2px;background:#e5e7eb;border-radius:2px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#0D1B3E,#2E5F9E);
  border-radius:2px;transition:width .45s cubic-bezier(.4,0,.2,1)}
.prog-lbl{font-size:12px;color:#bbb;white-space:nowrap;font-weight:500}

.step-body{flex:1}
.step-sec{font-size:11px;color:#bbb;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px;font-weight:600}
.step-q{font-size:28px;font-weight:600;line-height:1.2;margin-bottom:8px;color:#0D1B3E;letter-spacing:-.5px}
.step-hint{font-size:13px;color:#888;line-height:1.65;margin-bottom:30px}

.pills{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:30px}
.pill{padding:9px 22px;border:1.5px solid #e5e7eb;border-radius:999px;font-size:13px;
  background:#fff;color:#333;transition:all .12s;font-weight:500}
.pill:hover{border-color:#0D1B3E;color:#0D1B3E;background:#f0f3f8}
.pill.on{border:2px solid #0D1B3E;background:#0D1B3E;color:#fff}

.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(162px,1fr));gap:10px;margin-bottom:30px}
.card{border:1.5px solid #e5e7eb;border-radius:14px;padding:16px 15px 14px;background:#fff;
  text-align:left;transition:all .12s}
.card:hover{border-color:#0D1B3E;box-shadow:0 4px 16px rgba(13,27,62,.08)}
.card.on{border:2px solid #0D1B3E;background:#f0f3f8;box-shadow:0 4px 16px rgba(13,27,62,.12)}
.card-label{font-size:13px;font-weight:600;display:block;margin-bottom:5px;color:#111}
.card-sub{font-size:11px;color:#999;display:block;line-height:1.4}

.text-wrap{margin-bottom:30px}

.debt-group{margin-bottom:20px}
.debt-group-lbl{font-size:11px;color:#bbb;text-transform:uppercase;letter-spacing:.06em;margin-bottom:9px;font-weight:600}
.debt-rows{display:flex;flex-direction:column;gap:7px}
.drow{display:flex;align-items:center;gap:10px;padding:11px 15px;border:1.5px solid #e5e7eb;
  border-radius:10px;background:#fff;text-align:left;transition:all .12s}
.drow:hover{border-color:#0D1B3E}
.drow.on{border:2px solid #0D1B3E;background:#f0f3f8}
.dtog{width:18px;height:18px;border:1.5px solid #ddd;border-radius:4px;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;font-size:11px;
  background:#fff;color:#aaa;transition:all .12s;font-weight:700}
.drow.on .dtog{background:#0D1B3E;border-color:#0D1B3E;color:#fff}
.dname{font-size:13px;font-weight:600;flex:1;color:#111}
.dtag{font-size:11px;color:#bbb;background:#f5f5f5;padding:2px 8px;border-radius:999px}
.drow.on .dtag{background:#d8e4f0;color:#0D1B3E}
.damt{width:100px;padding:5px 9px;border:1.5px solid #ddd;border-radius:7px;
  font-size:12px;text-align:right;display:none;background:#fff;color:#111;font-weight:500}
.drow.on .damt{display:block;border-color:#0D1B3E}

.nav{display:flex;align-items:center;justify-content:space-between;padding-top:36px;margin-top:auto}
.btn-back{background:none;border:none;font-size:13px;color:#bbb;padding:8px 0;font-weight:500}
.btn-back:hover{color:#555}
.btn-next{background:linear-gradient(135deg,#0D1B3E,#1A3560);color:#fff;border:none;
  border-radius:10px;padding:12px 28px;font-size:13px;font-weight:600;
  transition:opacity .15s,transform .1s;letter-spacing:.2px}
.btn-next:hover:not(:disabled){opacity:.9;transform:translateY(-1px)}
.btn-next:active{transform:translateY(0)}

/* Summary */
.sum-section-title{font-size:11px;color:#bbb;text-transform:uppercase;letter-spacing:.07em;
  font-weight:600;margin:20px 0 10px;padding-bottom:6px;border-bottom:1px solid #f0f0f0}
.sum-row{display:flex;justify-content:space-between;align-items:center;
  padding:9px 0;border-bottom:1px solid #f7f7f7;font-size:13px}
.sum-row:last-child{border-bottom:none}
.sum-k{color:#999;font-weight:500}
.sum-v{color:#0D1B3E;font-weight:600;text-align:right;max-width:58%}
.dpill{display:inline-flex;padding:3px 10px;border-radius:999px;background:#eef1f8;
  border:1px solid #c8d4e8;font-size:11px;color:#0D1B3E;font-weight:600;margin:2px}
.gen-err{font-size:13px;color:#e74c3c;margin-top:14px;padding:10px 14px;
  background:#fdf2f2;border-radius:8px;border:1px solid #fcd0d0}

/* ── DONE ── */
#done{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.done-card{background:#fff;border-radius:20px;padding:52px 48px;width:440px;
  text-align:center;box-shadow:0 24px 80px rgba(0,0,0,.35)}
.done-icon{width:72px;height:72px;border-radius:50%;background:linear-gradient(135deg,#27ae60,#2ecc71);
  display:flex;align-items:center;justify-content:center;margin:0 auto 20px;
  font-size:32px;box-shadow:0 8px 24px rgba(39,174,96,.3)}
.done-title{font-size:24px;font-weight:600;color:#0D1B3E;margin-bottom:8px}
.done-sub{font-size:13px;color:#888;margin-bottom:8px}
.done-file{font-size:12px;color:#bbb;margin-bottom:32px;word-break:break-all;
  background:#f7f8fa;padding:8px 12px;border-radius:8px;font-family:monospace}
.btn-outline{width:100%;padding:12px;background:#fff;color:#0D1B3E;
  border:2px solid #0D1B3E;border-radius:10px;font-size:14px;font-weight:600;
  margin-top:10px;transition:background .15s}
.btn-outline:hover{background:#f0f3f8}

/* Spinner */
.spinner{display:inline-block;width:15px;height:15px;border:2px solid rgba(255,255,255,.3);
  border-top-color:#fff;border-radius:50%;animation:spin .65s linear infinite;
  vertical-align:middle;margin-right:8px}
@keyframes spin{to{transform:rotate(360deg)}}
.fade-in{animation:fi .25s ease}
@keyframes fi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* ── IMPORT SCREEN ── */
#import-screen{align-items:center;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%)}
.import-card{background:#fff;border-radius:20px;padding:48px 44px;width:560px;
  box-shadow:0 24px 80px rgba(0,0,0,.35)}
.import-header{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.import-logo{width:44px;height:44px;border-radius:10px;overflow:hidden;flex-shrink:0}
.import-logo img{width:100%;height:100%}
.import-title{font-size:22px;font-weight:600;color:#0D1B3E;letter-spacing:-.4px}
.import-sub{font-size:13px;color:#888;margin-top:2px}
.drop-zone{border:2px dashed #d0d8e8;border-radius:14px;padding:40px 24px;text-align:center;
  cursor:pointer;transition:all .2s;background:#fafbfc;margin-bottom:20px;position:relative}
.drop-zone:hover,.drop-zone.drag{border-color:#0D1B3E;background:#f0f3f8}
.drop-zone input[type=file]{position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%}
.drop-icon{font-size:36px;margin-bottom:12px}
.drop-title{font-size:15px;font-weight:600;color:#0D1B3E;margin-bottom:6px}
.drop-sub{font-size:12px;color:#aaa;line-height:1.6}
.drop-formats{display:flex;gap:6px;justify-content:center;margin-top:12px;flex-wrap:wrap}
.fmt-badge{padding:3px 10px;border-radius:999px;background:#eef1f8;border:1px solid #c8d4e8;
  font-size:11px;color:#0D1B3E;font-weight:600}
.import-file-info{display:none;align-items:center;gap:10px;padding:12px 16px;
  background:#f0f8f0;border:1.5px solid #27ae60;border-radius:10px;margin-bottom:16px}
.import-file-info.show{display:flex}
.file-icon{font-size:20px}
.file-name{font-size:13px;font-weight:600;color:#1a6b3a;flex:1}
.file-size{font-size:11px;color:#888}
.quality-panel{display:none;border-radius:12px;padding:18px 20px;margin-bottom:20px;border:1.5px solid}
.quality-panel.show{display:block}
.quality-panel.excellent{background:#f0faf4;border-color:#27ae60}
.quality-panel.bon{background:#f0f6ff;border-color:#2E5F9E}
.quality-panel.partiel{background:#fffbf0;border-color:#f39c12}
.quality-panel.insuffisant{background:#fff5f5;border-color:#e74c3c}
.quality-title{font-size:13px;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.quality-score{font-size:22px;font-weight:700}
.quality-items{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.q-item{display:flex;align-items:center;gap:5px;font-size:11px;padding:3px 9px;
  border-radius:999px;font-weight:500}
.q-item.ok{background:#d4edda;color:#1a6b3a}
.q-item.miss{background:#fce8e6;color:#c0392b}
.actuals-preview{display:none;margin-bottom:20px}
.actuals-preview.show{display:block}
.preview-title{font-size:12px;font-weight:600;color:#555;text-transform:uppercase;
  letter-spacing:.06em;margin-bottom:10px}
.preview-table{width:100%;border-collapse:collapse;font-size:12px}
.preview-table th{background:#f5f7fa;color:#888;font-weight:600;padding:6px 10px;
  text-align:right;font-size:11px;border-bottom:1px solid #eee}
.preview-table th:first-child{text-align:left}
.preview-table td{padding:7px 10px;border-bottom:1px solid #f5f5f5;color:#333}
.preview-table td:first-child{font-weight:500;color:#0D1B3E}
.preview-table td:not(:first-child){text-align:right;font-family:monospace;font-size:11px}
.preview-table tr:hover td{background:#fafafa}
.import-actions{display:flex;gap:10px;margin-top:4px}
.btn-secondary{flex:1;padding:12px;background:#f5f7fa;color:#0D1B3E;border:1.5px solid #d0d8e8;
  border-radius:10px;font-size:13px;font-weight:600;transition:all .15s}
.btn-secondary:hover{background:#e8edf5;border-color:#0D1B3E}
.import-err{font-size:13px;color:#e74c3c;padding:10px 14px;background:#fdf2f2;
  border-radius:8px;border:1px solid #fcd0d0;margin-bottom:14px;display:none}
.import-err.show{display:block}
.skip-link{text-align:center;margin-top:16px}
.skip-link button{background:none;border:none;font-size:12px;color:#bbb;text-decoration:underline;cursor:pointer}
.skip-link button:hover{color:#888}

/* ── SCENARIOS SCREEN ── */
#scenarios-screen{align-items:flex-start;justify-content:center;min-height:100vh;
  background:linear-gradient(135deg,#0a1628 0%,#0D1B3E 50%,#1a2d5a 100%);
  padding:32px 24px;overflow-y:auto}
.sc-wrap{width:100%;max-width:1100px;margin:0 auto}
.sc-top-bar{display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.06);
  border-radius:16px;padding:18px 24px;margin-bottom:24px;backdrop-filter:blur(8px)}
.sc-logo-sm{width:38px;height:38px;border-radius:9px;overflow:hidden;flex-shrink:0}
.sc-logo-sm img{width:100%;height:100%}
.sc-top-title{font-size:18px;font-weight:700;color:#fff;letter-spacing:-.3px}
.sc-top-sub{font-size:12px;color:#7799cc;margin-top:2px}
.sc-top-actions{margin-left:auto;display:flex;gap:10px}
.btn-sc-back{background:rgba(255,255,255,.1);color:#fff;border:none;border-radius:8px;
  padding:9px 18px;font-size:13px;font-weight:500;cursor:pointer;transition:background .15s;font-family:inherit}
.btn-sc-back:hover{background:rgba(255,255,255,.18)}
.btn-sc-gen{background:#fff;color:#0D1B3E;border:none;border-radius:8px;
  padding:9px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:opacity .15s;font-family:inherit}
.btn-sc-gen:hover:not(:disabled){opacity:.88}
.btn-sc-gen:disabled{opacity:.4;cursor:not-allowed}

/* 3-column grid */
.sc-grid{display:grid;grid-template-columns:200px 1fr 1fr 1fr;gap:0;
  background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 12px 48px rgba(0,0,0,.3)}
.sc-grid-header{display:contents}
.sc-col-label{background:#f8f9fa;border-right:1px solid #eee}
.sc-col-low{background:#fff5f5}
.sc-col-base{background:#f0f3f8}
.sc-col-best{background:#f0faf4}
.sc-col-head{padding:16px 14px;text-align:center;font-size:13px;font-weight:700;
  border-bottom:3px solid;display:flex;flex-direction:column;align-items:center;gap:4px}
.sc-col-head.label{background:#f8f9fa;border-color:#e0e0e0;text-align:left;
  justify-content:flex-end;font-size:11px;color:#aaa;text-transform:uppercase;letter-spacing:.06em}
.sc-col-head.low{border-color:#e74c3c;color:#c0392b;background:#fff5f5}
.sc-col-head.base{border-color:#0D1B3E;color:#0D1B3E;background:#eef1f8}
.sc-col-head.best{border-color:#27ae60;color:#27ae60;background:#f0faf4}
.sc-col-head .sc-icon{font-size:20px}
.sc-col-head .sc-head-label{font-size:14px}
.sc-col-head .sc-head-sub{font-size:10px;font-weight:400;opacity:.7}

/* Section rows */
.sc-section-row{display:contents}
.sc-section-cell{padding:10px 14px;font-size:11px;font-weight:700;
  text-transform:uppercase;letter-spacing:.07em;color:#fff;grid-column:1/-1;
  border-top:2px solid rgba(0,0,0,.05)}
.sc-section-cell.pl{background:#1A3560}
.sc-section-cell.nwc{background:#7B3F00}
.sc-section-cell.capex{background:#2C4A6E}
.sc-section-cell.debt{background:#7B0000}
.sc-section-cell.macro{background:#0D3349}

/* Param rows */
.sc-param-row{display:contents}
.sc-param-row:hover .sc-cell{background:#fafbfc}
.sc-param-row:hover .sc-cell.low{background:#fff0f0}
.sc-param-row:hover .sc-cell.base{background:#e8edf5}
.sc-param-row:hover .sc-cell.best{background:#e8f5ec}
.sc-cell{padding:8px 14px;border-bottom:1px solid #f0f0f0;display:flex;
  align-items:center;font-size:13px}
.sc-cell.label{color:#444;font-weight:500;border-right:1px solid #eee;
  justify-content:space-between}
.sc-cell .sc-unit{font-size:10px;color:#bbb;margin-left:4px}
.sc-cell.low{background:#fff5f5}
.sc-cell.base{background:#f0f3f8}
.sc-cell.best{background:#f0faf4}

/* Inputs */
.sc-input{width:100%;padding:5px 8px;border:1.5px solid transparent;border-radius:6px;
  font-size:13px;font-family:inherit;background:transparent;color:#111;
  text-align:right;transition:border .12s,background .12s;font-weight:500}
.sc-input:focus{outline:none;background:#fff;border-color:#0D1B3E}
.sc-cell.low .sc-input:focus{border-color:#e74c3c;background:#fff}
.sc-cell.best .sc-input:focus{border-color:#27ae60;background:#fff}
.sc-input.changed{font-weight:700}
.sc-input.low-val{color:#c0392b}
.sc-input.best-val{color:#27ae60}

/* Results */
.sc-results-bar{background:rgba(255,255,255,.06);border-radius:12px;
  padding:18px 24px;margin-top:20px;display:none}
.sc-results-bar.show{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.sc-results-title{font-size:13px;color:#fff;font-weight:600;margin-right:4px}
.sc-result-pill{display:flex;align-items:center;gap:8px;padding:8px 16px;
  border-radius:999px;font-size:12px;font-weight:600;cursor:pointer;
  border:none;font-family:inherit;transition:opacity .15s}
.sc-result-pill:hover{opacity:.85}
.sc-result-pill.low{background:#e74c3c;color:#fff}
.sc-result-pill.base{background:#fff;color:#0D1B3E}
.sc-result-pill.best{background:#27ae60;color:#fff}
.sc-err{background:rgba(231,76,60,.15);color:#ff8877;border-radius:8px;
  padding:10px 16px;font-size:13px;margin-top:12px;display:none}
.sc-err.show{display:block}
</style>
</head>
<body>
<div id="app">

<!-- LOGIN -->
<div id="login" class="screen active">
  <div class="login-card">
    <div class="login-logo"><img src="/assets/icon_256.png" alt="MG"></div>
    <div class="login-title">BP Generator</div>
    <div class="login-sub">Professional Business Plan Builder</div>
    <div class="login-by">by JRC Corporate Consulting</div>
    <label class="field-label">Code d'accès</label>
    <input id="license-input" class="field-input" type="text" placeholder="JRC-XXXX-XXXX" autocomplete="off">
    <div id="login-err" class="err-msg" style="display:none">⚠ <span id="err-text"></span></div>
    <button class="btn-primary" id="btn-login">Accéder à l'application →</button>
  </div>
  <div class="login-footer">© 2025 JRC Corporate Consulting — DIFC, Dubai</div>
</div>


<!-- IMPORT SCREEN -->
<div id="import-screen" class="screen">
  <div class="import-card">
    <div class="import-header">
      <div class="import-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div>
        <div class="import-title">Importer les données financières</div>
        <div class="import-sub">Excel, CSV ou PDF — les actuals pré-rempliront le modèle</div>
      </div>
    </div>

    <div class="drop-zone" id="drop-zone">
      <input type="file" id="file-input" accept=".xlsx,.xls,.xlsm,.csv,.txt,.tsv,.pdf">
      <div class="drop-icon">📂</div>
      <div class="drop-title">Glisse ton fichier ici ou clique pour parcourir</div>
      <div class="drop-sub">P&L, Bilan, Cash Flow — n'importe quelle structure<br>Le moteur reconnaît automatiquement les lignes financières</div>
      <div class="drop-formats">
        <span class="fmt-badge">Excel .xlsx</span>
        <span class="fmt-badge">CSV</span>
        <span class="fmt-badge">PDF</span>
      </div>
    </div>

    <div class="import-file-info" id="file-info">
      <span class="file-icon">📄</span>
      <span class="file-name" id="file-name-lbl"></span>
      <span class="file-size" id="file-size-lbl"></span>
    </div>

    <div class="import-err" id="import-err"></div>

    <div class="quality-panel" id="quality-panel">
      <div class="quality-title">
        <span id="quality-label"></span>
        <span class="quality-score" id="quality-score"></span>
        <span style="font-size:12px;color:#888;font-weight:400">/ 100</span>
      </div>
      <div class="quality-items" id="quality-items"></div>
    </div>

    <div class="actuals-preview" id="actuals-preview">
      <div class="preview-title">Aperçu des données extraites</div>
      <table class="preview-table" id="preview-table">
        <thead id="preview-head"></thead>
        <tbody id="preview-body"></tbody>
      </table>
    </div>

    <div class="import-actions">
      <button class="btn-secondary" id="btn-reupload" style="display:none">↩ Changer de fichier</button>
      <button class="btn-primary" id="btn-use-data" style="display:none">Utiliser ces données → Configurer le BP</button>
    </div>
    <button class="btn-primary" id="btn-analyze" style="display:none;width:100%;margin-top:0">Analyser le fichier →</button>

    <div class="skip-link">
      <button id="btn-skip-import">Passer cette étape — saisir les données manuellement</button>
    </div>
  </div>
</div>

<!-- WIZARD -->
<div id="wizard" class="screen">
  <div class="sidebar">
    <div class="side-brand">
      <div class="side-logo"><img src="/assets/icon_256.png" alt="MG"></div>
      <div class="side-brand-text">
        <div class="side-name">BP Generator</div>
        <div class="side-tag">JRC Corporate</div>
      </div>
    </div>
    <div class="side-steps" id="side-steps"></div>
    <div class="side-bottom">
      <div class="side-user">Connecté en tant que</div>
      <div class="side-user-name" id="side-user-name">—</div>
    </div>
  </div>
  <div class="main">
    <div class="prog-wrap">
      <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
      <div class="prog-lbl" id="prog-lbl"></div>
    </div>
    <div id="step-content" class="step-body fade-in"></div>
    <div class="nav">
      <button class="btn-back" id="btn-back">← Retour</button>
      <button class="btn-next" id="btn-next">Suivant →</button>
    </div>
  </div>
</div>

<!-- DONE -->
<div id="done" class="screen">
  <div class="done-card">
    <div class="done-icon">✓</div>
    <div class="done-title">Modèle généré !</div>
    <div class="done-sub">Ton fichier Excel est prêt</div>
    <div class="done-file" id="done-filename"></div>
    <button class="btn-primary" id="btn-download">⬇ Télécharger le fichier Excel</button>
    <button class="btn-primary" id="btn-preview" onclick="loadPreview(currentFilename)" style="background:linear-gradient(135deg,#2E5F9E,#1A3560)">👁 Voir l'aperçu du modèle</button>
      <button class="btn-primary" id="btn-scenarios" onclick="showScreen('scenarios-screen')" style="background:linear-gradient(135deg,#27ae60,#2ecc71);margin-top:0">📊 Générer Low / Base / Best Case</button>
      <button class="btn-outline" id="btn-new">+ Nouveau modèle</button>
  </div>
</div>

</div>
<script>
const API='';let licenseKey='',currentUser='',currentFilename='';
const STEPS=[
  {id:'name',sec:'Identité',q:'Quel est le nom de la société ou du projet ?',hint:"Tel qu'il apparaîtra en en-tête de chaque onglet Excel.",type:'text',f:'company_name',ph:'ex. JBF Global Europe — Industrial BP'},
  {id:'type',sec:'Type de modèle',q:'Quel type de business plan ?',hint:'Détermine les drivers de revenus et la structure du modèle.',type:'cards',f:'business_type',multi:false,opts:[
    {v:'industrial',l:'Industriel',s:'Volume MT, spread, capacité'},{v:'lbo',l:'LBO / M&A',s:'Leveraged buyout, IRR/MOIC'},
    {v:'saas',l:'SaaS / Tech',s:'ARR, churn, LTV/CAC'},{v:'immo',l:'Immobilier',s:'Loyers/m², LTV, rendement'},
    {v:'restr',l:'Restructuring',s:'SSFA, haircut, PIK, covenants'},{v:'retail',l:'Retail',s:'Magasins, panier moyen, SSS'}]},
  {id:'ccy',sec:'Paramètres',q:'Devise de reporting ?',type:'pills',f:'currency',multi:false,opts:['USD','EUR','GBP','AED','BHD','SAR']},
  {id:'yrs',sec:'Paramètres',q:'Horizon de projection ?',hint:"Nombre d'années de business plan.",type:'pills',f:'n_years',multi:false,opts:['3 ans','5 ans','7 ans','10 ans']},
  {id:'fy',sec:'Paramètres',q:"Mois de début d'exercice fiscal ?",hint:'Janvier = calendaire. Avril = fiscal UK/Bahreïn.',type:'pills',f:'fy_start_month',multi:false,opts:['Janvier','Février','Mars','Avril','Juillet','Octobre']},
  {id:'mods',sec:'Modules',q:'Quels modules inclure ?',hint:'P&L, BS et CF sont toujours actifs.',type:'cards',f:'modules',multi:true,opts:[
    {v:'debt',l:'Debt schedule',s:'Multi-tranche, covenants, sweep'},{v:'nwc',l:'NWC',s:'DSO / DIO / DPO'},
    {v:'capex',l:'CAPEX',s:"Plan d'invest. & amortissements"},{v:'tax',l:'Fiscalité',s:'IS, impôt différé, déficits'},
    {v:'scenarios',l:'Scénarios',s:'Low / Base / High'},{v:'returns',l:'Returns / LBO',s:'IRR, MOIC, waterfall equity'},
    {v:'valuation',l:'Valorisation',s:'DCF + EV/EBITDA exit bridge'},{v:'consol',l:'Consolidation',s:'Multi-entités + éliminations'}]},
  {id:'debt',sec:'Financement',q:'Quelles tranches de dette activer ?',hint:'Coche chaque tranche et saisis le montant en milliers.',type:'debt',f:'debt',groups:[
    {lbl:'Senior sécurisée',items:[{k:'tla',l:'Term Loan A',t:'Amortissable',d:150000},{k:'tlb',l:'Term Loan B',t:'Bullet',d:0},{k:'ss',l:'Super Senior (SSFA)',t:'Prioritaire',d:0},{k:'rcf',l:'RCF',t:'Revolving',d:40000},{k:'mur',l:'Murabaha islamique',t:'Islamic',d:0}]},
    {lbl:'Mezzanine / Subordonné',items:[{k:'mez',l:'Mezzanine cash pay',t:'Mezz',d:0},{k:'pik',l:'PIK toggle',t:'PIK',d:0},{k:'shl',l:'SHL (shareholder)',t:'Full PIK',d:0},{k:'uni',l:'Unitranche',t:'Blended',d:0}]},
    {lbl:'Capital markets / Restructuring',items:[{k:'hyb',l:'High Yield Bond',t:'HYB',d:0},{k:'dip',l:'New money (DIP-style)',t:'Super senior',d:0},{k:'d2e',l:'Debt-to-equity swap',t:'Haircut',d:0}]}]},
  {id:'mech',sec:'Mécaniques',q:'Quelles mécaniques de dette activer ?',type:'cards',f:'mechanics',multi:true,opts:[
    {v:'sweep',l:'Cash sweep',s:'Remboursement sur FCF excédentaire'},{v:'ratchet',l:'Margin ratchet',s:'Marge liée au niveau de levier'},
    {v:'cov',l:'Covenant tracking',s:'Levier, ICR, DSCR + flags'},{v:'oid',l:'OID / upfront fees',s:'Amortissement sur durée'},
    {v:'fx',l:'Couverture FX',s:'Multi-devise par tranche'},{v:'irs',l:'Swap taux fixe/flottant',s:'Interest rate swap'}]},
  {id:'rate',sec:'Mécaniques',q:'Quel taux de référence ?',type:'pills',f:'base_rate_index',multi:false,opts:['SOFR','EURIBOR 3M','EURIBOR 6M','SONIA','Taux fixe']},
  {id:'fmt',sec:'Format',q:'Granularité du modèle ?',type:'cards',f:'output_format',multi:false,opts:[
    {v:'annual',l:'Annuel uniquement',s:'Standard IM boutique, plus lisible'},{v:'monthly',l:'Mensuel + annuel',s:'Détail opérationnel complet'},{v:'quarterly',l:'Trimestriel + annuel',s:'Fréquence intermédiaire'}]},
  {id:'sum',sec:'Récapitulatif',q:'Tout est bon ?',hint:'Vérifie la configuration avant de lancer la génération.',type:'summary'}
];
const YRS={'3 ans':3,'5 ans':5,'7 ans':7,'10 ans':10};
const MNTH={'Janvier':1,'Février':2,'Mars':3,'Avril':4,'Juillet':7,'Octobre':10};
let answers={},stepIdx=0;
function visibleSteps(){const h=(answers.modules||[]).includes('debt');return STEPS.filter(s=>(['debt','mech','rate'].includes(s.id)?h:true));}
document.getElementById('btn-login').onclick=doLogin;
document.getElementById('license-input').onkeydown=e=>e.key==='Enter'&&doLogin();
async function doLogin(){
  const key=document.getElementById('license-input').value.trim();
  const errEl=document.getElementById('login-err');const errTxt=document.getElementById('err-text');
  const btn=document.getElementById('btn-login');
  if(!key)return;
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Vérification...';
  errEl.style.display='none';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({license_key:key})});
    const d=await r.json();if(!r.ok)throw new Error(d.detail||'Erreur');
    licenseKey=key;currentUser=d.user;
    document.getElementById('side-user-name').textContent=d.user;
    showScreen('wizard');renderStep();
  }catch(e){errTxt.textContent=e.message;errEl.style.display='flex';}
  btn.disabled=false;btn.textContent='Accéder à l\'application →';}
function showScreen(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active');}
document.getElementById('btn-next').onclick=onNext;
document.getElementById('btn-back').onclick=onBack;
function onNext(){const vs=visibleSteps();const s=vs[stepIdx];if(s.type==='summary'){doGenerate();return;}if(stepIdx<vs.length-1){stepIdx++;renderStep();}}
function onBack(){if(stepIdx>0){stepIdx--;renderStep();}}
function renderStep(){
  const vs=visibleSteps();const s=vs[stepIdx];const pct=Math.round((stepIdx/(vs.length-1))*100);
  document.getElementById('prog-fill').style.width=pct+'%';
  document.getElementById('prog-lbl').textContent=(stepIdx+1)+' / '+vs.length;
  document.getElementById('btn-back').style.visibility=stepIdx===0?'hidden':'visible';
  const nb=document.getElementById('btn-next');
  nb.textContent=s.type==='summary'?'Générer le modèle Excel →':'Suivant →';
  nb.disabled=!canAdvance(s);
  document.getElementById('side-steps').innerHTML=vs.map((st,i)=>
    `<div class="side-step ${i<stepIdx?'done':i===stepIdx?'active':''}">`+
    '<div class="side-dot"></div>'+st.sec+'</div>').join('');
  const el=document.getElementById('step-content');
  el.className='step-body fade-in';void el.offsetWidth;
  el.innerHTML=buildHTML(s);attachEvents(s);
  if(s.type==='text'){const inp=el.querySelector('input');if(inp){inp.focus();inp.oninput=()=>{answers[s.f]=inp.value;nb.disabled=!inp.value.trim();};inp.onkeydown=e=>e.key==='Enter'&&!nb.disabled&&onNext();}}}
function canAdvance(s){
  if(s.type==='text')return!!(answers[s.f]||'').trim();
  if(['summary','debt'].includes(s.type))return true;
  if(s.multi)return(answers[s.f]||[]).length>0;
  return!!answers[s.f];}
function buildHTML(s){
  const sec=`<div class="step-sec">${s.sec}</div>`;
  const q=`<div class="step-q">${s.q}</div>`;
  const hint=s.hint?`<div class="step-hint">${s.hint}</div>`:'';
  if(s.type==='text')return sec+q+hint+`<div class="text-wrap"><input class="field-input" id="txt" value="${answers[s.f]||''}" placeholder="${s.ph||''}" style="font-size:15px;padding:13px 15px"></div>`;
  if(s.type==='pills'){const cur=answers[s.f];return sec+q+hint+'<div class="pills">'+s.opts.map(o=>`<button class="pill${cur===o?' on':''}" data-v="${o}">${o}</button>`).join('')+'</div>';}
  if(s.type==='cards'){const cur=answers[s.f]||(s.multi?[]:null);return sec+q+hint+'<div class="cards">'+s.opts.map(o=>{const sel=s.multi?(cur||[]).includes(o.v):cur===o.v;return`<button class="card${sel?' on':''}" data-v="${o.v}"><span class="card-label">${o.l}</span><span class="card-sub">${o.s}</span></button>`;}).join('')+'</div>';}
  if(s.type==='debt'){const cur=answers.debt||{};return sec+q+hint+s.groups.map(g=>'<div class="debt-group"><div class="debt-group-lbl">'+g.lbl+'</div><div class="debt-rows">'+g.items.map(item=>{const on=cur[item.k]!==undefined;return`<button class="drow${on?' on':''}" data-k="${item.k}" data-d="${item.d}"><div class="dtog">${on?'✓':''}</div><span class="dname">${item.l}</span><span class="dtag">${item.t}</span><input class="damt" type="number" value="${on?cur[item.k]:item.d}" placeholder="Montant k" min="0" step="1000"></button>`;}).join('')+'</div></div>').join('');}
  if(s.type==='summary'){
    const d=answers;const debt=d.debt||{};
    const dp=Object.entries(debt).map(([k,v])=>`<span class="dpill">${k.toUpperCase()} — ${Number(v).toLocaleString()}k</span>`).join('')||'<span style="color:#bbb;font-size:12px">Aucune tranche</span>';
    return sec+q+hint+
      '<div class="sum-section-title">Identité & horizon</div>'+
      [['Société',d.company_name],['Type',d.business_type],['Devise',d.currency],['Horizon',d.n_years],['Exercice fiscal',d.fy_start_month]].map(([k,v])=>`<div class="sum-row"><span class="sum-k">${k}</span><span class="sum-v">${v||'—'}</span></div>`).join('')+
      '<div class="sum-section-title">Modules & format</div>'+
      [['Modules',(d.modules||[]).join(', ')||'—'],['Mécaniques',(d.mechanics||[]).join(', ')||'—'],['Taux de ref.',d.base_rate_index],['Format',d.output_format]].map(([k,v])=>`<div class="sum-row"><span class="sum-k">${k}</span><span class="sum-v">${v||'—'}</span></div>`).join('')+
      '<div class="sum-section-title">Tranches de dette</div>'+
      `<div style="padding:8px 0">${dp}</div>`+
      '<div id="gen-err" class="gen-err" style="display:none"></div>';
  }return'';}
function attachEvents(s){
  const nb=document.getElementById('btn-next');
  if(s.type==='pills')document.querySelectorAll('.pill').forEach(b=>{b.onclick=()=>{document.querySelectorAll('.pill').forEach(x=>x.classList.remove('on'));b.classList.add('on');answers[s.f]=b.dataset.v;nb.disabled=false;};});
  if(s.type==='cards')document.querySelectorAll('.card').forEach(b=>{b.onclick=()=>{if(s.multi){b.classList.toggle('on');answers[s.f]=[...document.querySelectorAll('.card.on')].map(x=>x.dataset.v);nb.disabled=(answers[s.f]||[]).length===0;}else{document.querySelectorAll('.card').forEach(x=>x.classList.remove('on'));b.classList.add('on');answers[s.f]=b.dataset.v;nb.disabled=false;}};});
  if(s.type==='debt')document.querySelectorAll('.drow').forEach(row=>{
    row.onclick=e=>{if(e.target.tagName==='INPUT')return;const k=row.dataset.k;const def=parseInt(row.dataset.d)||0;const cur=answers.debt||{};if(cur[k]!==undefined){const n={...cur};delete n[k];answers.debt=n;row.classList.remove('on');row.querySelector('.dtog').textContent='';}else{const inp=row.querySelector('.damt');answers.debt={...cur,[k]:inp?parseInt(inp.value)||def:def};row.classList.add('on');row.querySelector('.dtog').textContent='✓';}};
    const inp=row.querySelector('.damt');if(inp)inp.oninput=e=>{e.stopPropagation();const k=row.dataset.k;if(answers.debt&&answers.debt[k]!==undefined)answers.debt[k]=parseInt(inp.value)||0;};});}
async function doGenerate(){
  const btn=document.getElementById('btn-next');const errEl=document.getElementById('gen-err');
  btn.disabled=true;btn.innerHTML='<span class="spinner"></span>Génération en cours...';
  if(errEl)errEl.style.display='none';
  const payload={company_name:answers.company_name||'Business Plan',business_type:answers.business_type||'industrial',currency:answers.currency||'USD',n_years:YRS[answers.n_years]||7,fy_start_month:MNTH[answers.fy_start_month]||1,modules:answers.modules||[],debt:answers.debt||{},mechanics:answers.mechanics||[],base_rate_index:answers.base_rate_index||'SOFR',output_format:answers.output_format||'annual'};
  try{
    const r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json','x-license':licenseKey},body:JSON.stringify(payload)});
    const d=await r.json();if(!r.ok)throw new Error(d.detail||'Erreur génération');
    currentFilename=d.filename;document.getElementById('done-filename').textContent=d.filename;showScreen('done');
  }catch(e){if(errEl){errEl.textContent='⚠ '+e.message;errEl.style.display='block';}btn.disabled=false;btn.textContent='Générer le modèle Excel →';}
}
document.getElementById('btn-download').onclick=()=>{
  fetch(`/api/download/${currentFilename}`,{headers:{'x-license':licenseKey}}).then(r=>r.blob()).then(blob=>{const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=currentFilename;document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);});};
document.getElementById('btn-new').onclick=()=>{answers={};stepIdx=0;showScreen('wizard');renderStep();};

// ── IMPORT MODULE ─────────────────────────────────────────────────────────────
let importedData = null;
let selectedFile = null;

const dropZone  = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

// Drag and drop
dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('drag'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('drag');
  const f = e.dataTransfer.files[0];
  if (f) handleFileSelect(f);
});
fileInput.addEventListener('change', e => {
  if (e.target.files[0]) handleFileSelect(e.target.files[0]);
});

function handleFileSelect(file) {
  selectedFile = file;
  const info = document.getElementById('file-info');
  document.getElementById('file-name-lbl').textContent = file.name;
  document.getElementById('file-size-lbl').textContent = (file.size/1024).toFixed(1) + ' KB';
  info.classList.add('show');
  document.getElementById('btn-analyze').style.display = 'block';
  document.getElementById('btn-reupload').style.display = 'none';
  document.getElementById('btn-use-data').style.display = 'none';
  document.getElementById('quality-panel').classList.remove('show');
  document.getElementById('actuals-preview').classList.remove('show');
  document.getElementById('import-err').classList.remove('show');
}

document.getElementById('btn-analyze').onclick = async () => {
  if (!selectedFile) return;
  const btn = document.getElementById('btn-analyze');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Analyse en cours...';

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const r = await fetch('/api/import', {
      method: 'POST',
      headers: { 'x-license': licenseKey },
      body: formData,
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur extraction');

    importedData = d;
    showQualityPanel(d.data_quality);
    showActualsPreview(d.actuals_overlay, d.hist_years);

    document.getElementById('btn-analyze').style.display = 'none';
    document.getElementById('btn-reupload').style.display = 'block';
    document.getElementById('btn-use-data').style.display = 'block';
  } catch(e) {
    const errEl = document.getElementById('import-err');
    errEl.textContent = '⚠ ' + e.message;
    errEl.classList.add('show');
  }
  btn.disabled = false;
  btn.innerHTML = 'Analyser le fichier →';
};

function showQualityPanel(q) {
  const panel = document.getElementById('quality-panel');
  panel.className = 'quality-panel show ' + q.label.toLowerCase();
  document.getElementById('quality-label').textContent = 'Qualité des données : ' + q.label;
  document.getElementById('quality-score').textContent = q.score;

  const coreKeys = ['revenue','ebitda','net_income','gross_profit','ebit',
                    'depreciation','gross_debt','cash','capex','operating_cf'];
  const labels = {
    revenue:'Revenus', ebitda:'EBITDA', net_income:'Résultat net',
    gross_profit:'Marge brute', ebit:'EBIT', depreciation:'D&A',
    gross_debt:'Dette brute', cash:'Trésorerie', capex:'Capex',
    operating_cf:'Cash opérationnel', trade_receivables:'Créances clients',
    inventories:'Stocks', trade_payables:'Dettes fourn.'
  };
  const items = document.getElementById('quality-items');
  items.innerHTML = '';
  for (const [key, present] of Object.entries(q.present)) {
    if (!coreKeys.includes(key) && !['trade_receivables','inventories','trade_payables'].includes(key)) continue;
    const span = document.createElement('span');
    span.className = 'q-item ' + (present ? 'ok' : 'miss');
    span.textContent = (present ? '✓ ' : '✗ ') + (labels[key] || key);
    items.appendChild(span);
  }
}

function fmt(v) {
  if (v === null || v === undefined) return '—';
  const n = parseFloat(v);
  if (isNaN(n)) return '—';
  if (Math.abs(n) >= 1000000) return (n/1000000).toFixed(1) + 'M';
  if (Math.abs(n) >= 1000)    return (n/1000).toFixed(0) + 'k';
  return n.toFixed(1);
}

function showActualsPreview(actuals, years) {
  const preview = document.getElementById('actuals-preview');
  const thead = document.getElementById('preview-head');
  const tbody = document.getElementById('preview-body');

  const rowLabels = {
    revenue:'Revenus', gross_profit:'Marge brute', ebitda:'EBITDA',
    ebitda_margin:'Marge EBITDA %', ebit:'EBIT', net_income:'Résultat net',
    gross_debt:'Dette brute', cash:'Trésorerie', net_debt:'Dette nette',
    capex:'Capex', net_leverage:'Levier net'
  };

  thead.innerHTML = '<tr><th>Indicateur</th>' +
    years.map(y => `<th>${y}</th>`).join('') + '</tr>';

  tbody.innerHTML = '';
  for (const [key, label] of Object.entries(rowLabels)) {
    const hasData = years.some(y => actuals[y] && actuals[y][key] !== undefined);
    if (!hasData) continue;
    const tr = document.createElement('tr');
    const isPct = key.includes('margin') || key.includes('leverage');
    const cells = years.map(y => {
      const v = actuals[y] ? actuals[y][key] : null;
      if (v === null || v === undefined) return '<td>—</td>';
      if (isPct) return `<td>${(v*100).toFixed(1)}%</td>`;
      return `<td>${fmt(v)}</td>`;
    }).join('');
    tr.innerHTML = `<td>${label}</td>${cells}`;
    tbody.appendChild(tr);
  }

  preview.classList.add('show');
}

document.getElementById('btn-reupload').onclick = () => {
  selectedFile = null; importedData = null;
  fileInput.value = '';
  document.getElementById('file-info').classList.remove('show');
  document.getElementById('quality-panel').classList.remove('show');
  document.getElementById('actuals-preview').classList.remove('show');
  document.getElementById('btn-analyze').style.display = 'none';
  document.getElementById('btn-reupload').style.display = 'none';
  document.getElementById('btn-use-data').style.display = 'none';
  document.getElementById('import-err').classList.remove('show');
};

document.getElementById('btn-use-data').onclick = () => {
  if (importedData) {
    // Pre-fill answers from imported data
    const p = importedData.proj_assumptions;
    const la = importedData.last_actuals;
    answers._imported = importedData;
    // Will be used by generate endpoint
  }
  showScreen('wizard');
  renderStep();
};

document.getElementById('btn-skip-import').onclick = () => {
  showScreen('wizard');
  renderStep();
};

// Override doLogin to go to import screen first
const _origDoLogin = doLogin;
doLogin = async function() {
  const key = document.getElementById('license-input').value.trim();
  const errEl = document.getElementById('login-err');
  const errTxt = document.getElementById('err-text');
  const btn = document.getElementById('btn-login');
  if (!key) return;
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Vérification...';
  errEl.style.display = 'none';
  try {
    const r = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({license_key: key})
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur');
    licenseKey = key; currentUser = d.user;
    document.getElementById('side-user-name').textContent = d.user;
    showScreen('import-screen');  // Go to import screen first
  } catch(e) {
    errTxt.textContent = e.message;
    errEl.style.display = 'flex';
  }
  btn.disabled = false;
  btn.textContent = "Accéder à l'application →";
};

// Patch generate to include imported data
const _origDoGenerate = doGenerate;
doGenerate = async function() {
  // If we have imported data, merge proj assumptions into payload
  if (importedData && importedData.proj_assumptions) {
    const p = importedData.proj_assumptions;
    answers._proj = p;
  }
  await _origDoGenerate();
};


// ── SCENARIOS MODULE ──────────────────────────────────────────────────────────
let selectedScenarios = new Set(['low','base','best']);
let lastBaseConfig = null;
let scenarioFiles = {};

function toggleScenario(sk) {
  const box = document.querySelector(`.sc-box.${sk}`);
  if (selectedScenarios.has(sk)) {
    if (selectedScenarios.size <= 1) return; // keep at least one
    selectedScenarios.delete(sk);
    box.classList.remove('selected');
  } else {
    selectedScenarios.add(sk);
    box.classList.add('selected');
  }
}

document.getElementById('btn-gen-scenarios').onclick = generateScenarios;

async function generateScenarios() {
  const btn = document.getElementById('btn-gen-scenarios');
  const errEl = document.getElementById('sc-err');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Génération en cours...';
  errEl.classList.remove('show');

  if (!lastBaseConfig) {
    errEl.textContent = '⚠ Aucune configuration de base trouvée. Génère d'abord un modèle.';
    errEl.classList.add('show');
    btn.disabled = false; btn.textContent = 'Générer les scénarios sélectionnés →';
    return;
  }

  try {
    const r = await fetch('/api/generate-scenarios', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-license': licenseKey },
      body: JSON.stringify({
        base_config: lastBaseConfig,
        scenarios: [...selectedScenarios],
        generate_separate: true,
      }),
    });
    const d = await r.json();
    if (!r.ok) throw new Error(d.detail || 'Erreur génération');

    scenarioFiles = {};
    d.files.forEach(f => { scenarioFiles[f.scenario] = f; });
    showScenarioResults(d.files);
    document.getElementById('sc-results').classList.add('show');
  } catch(e) {
    errEl.textContent = '⚠ ' + e.message;
    errEl.classList.add('show');
  }
  btn.disabled = false;
  btn.textContent = 'Générer les scénarios sélectionnés →';
}

function showScenarioResults(files) {
  const icons = { low:'📉', base:'📊', best:'📈' };
  const list = document.getElementById('sc-result-list');
  list.innerHTML = files.map(f => `
    <div class="sc-result-item ${f.scenario}">
      <span class="sc-result-icon">${icons[f.scenario]||'📄'}</span>
      <div>
        <div class="sc-result-name ${f.scenario}">${f.label}</div>
        <div class="sc-result-file">${f.filename}</div>
      </div>
      <button class="btn-dl ${f.scenario}" onclick="downloadScenario('${f.filename}')">
        ⬇ Télécharger
      </button>
    </div>
  `).join('');
}

async function downloadScenario(filename) {
  const r = await fetch('/api/download/' + filename, { headers: { 'x-license': licenseKey } });
  const blob = await r.blob();
  const u = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = u; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(u);
}

// ── Patch done screen to add "Générer scénarios" button ──────────────────────
const _origShowDone = showScreen;
const _patchedGenerate = doGenerate;

// Store last config when generating
const __origDoGenerate = doGenerate;
doGenerate = async function() {
  // Build and store the payload as lastBaseConfig
  const YRS_MAP2  = {'3 ans':3,'5 ans':5,'7 ans':7,'10 ans':10};
  const MNTH_MAP2 = {'Janvier':1,'Février':2,'Mars':3,'Avril':4,'Juillet':7,'Octobre':10};
  lastBaseConfig = {
    company_name:    answers.company_name    || 'Business Plan',
    business_type:   answers.business_type   || 'industrial',
    currency:        answers.currency        || 'USD',
    units:           'k',
    fy_start_month:  MNTH_MAP2[answers.fy_start_month] || 1,
    proj_start_year: new Date().getFullYear(),
    n_years:         YRS_MAP2[answers.n_years] || 7,
    actuals_end_year:  new Date().getFullYear() - 1,
    actuals_end_month: (MNTH_MAP2[answers.fy_start_month] || 1) - 1 || 12,
    freq: 'Annual',
    modules: {
      debt:      (answers.modules||[]).includes('debt')      ? 1 : 0,
      tax:       (answers.modules||[]).includes('tax')       ? 1 : 0,
      scenarios: 1,
      returns:   (answers.modules||[]).includes('returns')   ? 1 : 0,
      valuation: (answers.modules||[]).includes('valuation') ? 1 : 0,
      consol:    (answers.modules||[]).includes('consol')    ? 1 : 0,
    },
    revenue: {
      capacity_mt:   Array(YRS_MAP2[answers.n_years]||7).fill(220000),
      base_volume:   Array(YRS_MAP2[answers.n_years]||7).fill(180000),
      volume_growth: Array(YRS_MAP2[answers.n_years]||7).fill(0.03),
      price_per_mt:  Array(YRS_MAP2[answers.n_years]||7).fill(1050),
      freight_mt:    Array(YRS_MAP2[answers.n_years]||7).fill(35),
      commission_pct:Array(YRS_MAP2[answers.n_years]||7).fill(0.01),
    },
    costs: {
      direct_mat_mt:[520,535,548,558,565,572,578].slice(0,YRS_MAP2[answers.n_years]||7),
      direct_mat_gr: Array(YRS_MAP2[answers.n_years]||7).fill(0.02),
      utilities_mt:  Array(YRS_MAP2[answers.n_years]||7).fill(45),
      packing_mt:    Array(YRS_MAP2[answers.n_years]||7).fill(18),
      var_opex_other_mt: Array(YRS_MAP2[answers.n_years]||7).fill(12),
      staff_prod:    Array(YRS_MAP2[answers.n_years]||7).fill(8500),
      staff_sga:     Array(YRS_MAP2[answers.n_years]||7).fill(3200),
      headcount_gr:  Array(YRS_MAP2[answers.n_years]||7).fill(0.02),
      maintenance:   Array(YRS_MAP2[answers.n_years]||7).fill(2400),
      insurance:     Array(YRS_MAP2[answers.n_years]||7).fill(800),
      rent:          Array(YRS_MAP2[answers.n_years]||7).fill(600),
      it:            Array(YRS_MAP2[answers.n_years]||7).fill(400),
      prof_fees:     Array(YRS_MAP2[answers.n_years]||7).fill(350),
      other_sga:     Array(YRS_MAP2[answers.n_years]||7).fill(500),
      restr:         Array(YRS_MAP2[answers.n_years]||7).fill(0),
    },
    nwc:   {dso:[50],dio:[35],dpo:[55],oca_pct:[0.01],ocl_pct:[0.02]},
    capex: {maint:[3500],expan:[8000],opening_ppe:95000,useful_life:20,accum_dep_open:28000},
    tax:   {rate:[0.25],loss_cf_open:0,dt_rate:[0.25]},
    macro: {cpi:[0.025],fx_usd_eur:[1.09],fx_usd_gbp:[1.27],fx_usd_aed:[3.67]},
    debt:  answers.debt ? Object.fromEntries(Object.entries(answers.debt).map(([k,v])=>([k,{active:1,amount:parseInt(v),currency:answers.currency||'USD',tenor_yrs:7,margin_pct:0.0325,pik_margin_pct:0}]))) : {},
    debt_mechanics: {
      base_rate_index:   answers.base_rate_index || 'SOFR',
      base_rate_pct:     0.045, base_rate_floor: 0.0,
      upfront_fee_pct:   0.015, commit_fee_pct: 0.005, oid_pct: 0.0,
      cash_sweep_pct:    0.75,
      cash_sweep_active: (answers.mechanics||[]).includes('sweep')   ? 1 : 0,
      margin_ratchet:    (answers.mechanics||[]).includes('ratchet') ? 1 : 0,
      covenant_tracking: (answers.mechanics||[]).includes('cov')     ? 1 : 0,
      lev_covenant: 5.0, icr_covenant: 2.0, dscr_covenant: 0.0,
      fx_hedge:   (answers.mechanics||[]).includes('fx')  ? 1 : 0,
      irs_active: (answers.mechanics||[]).includes('irs') ? 1 : 0,
    },
  };
  // Expand single-value arrays to n_years
  const n = lastBaseConfig.n_years;
  ['nwc','capex','tax','macro'].forEach(section => {
    const s = lastBaseConfig[section];
    if (s) Object.keys(s).forEach(k => {
      if (Array.isArray(s[k]) && s[k].length === 1) s[k] = Array(n).fill(s[k][0]);
    });
  });
  await __origDoGenerate();
};

</script>
</body>
</html>