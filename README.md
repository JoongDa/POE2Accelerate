# POE2 Host Accelerator / POE2 加速 Hosts /POEHostUpdater

## 简介 / Description

**中文：**  
本项目用于解析 `patch-poe2.poecdn.com` 的 IP 并将其写入本地 `hosts` 文件，以加速 Path of Exile 2 (POE2) 客户端的更新和下载。  
- 自动解析域名 IP  
- 使用 ping 测延迟，选择最快的 IP（可选）  
- 可生成可追加到 hosts 的内容  
- 刷新HOSTS
- 
**English:**  
This project resolves the IP addresses of `patch-poe2.poecdn.com` and writes them to your local `hosts` file, helping to accelerate Path of Exile 2 (POE2) client updates and downloads.  
- Automatically resolve domain IPs  
- Optionally select the fastest IP based on ping  
- Generate content that can be appended to the hosts file  
- SYNC HOSTS
---

## 功能 / Features

- 解析 POE2 更新 CDN 域名到 IP  
- 自动选择延迟最低的 IP（最快连接）  
- 支持将 IP 写入 hosts 文件（Windows / Linux / Mac）  
- 可生成文本文件供手动追加 hosts（无需管理员权限）  

**English:**  
- Resolve POE2 update CDN domain to IPs  
- Automatically select the fastest IP based on ping  
- Supports writing IP to the hosts file (Windows/Linux/Mac)  
- Can generate a text file for manual hosts update (no admin rights needed)  

---

## 使用方法 / Usage

### 方法 1：自动写入 hosts（需要管理员权限 / Admin required）
```bash
# Windows PowerShell / CMD
python main.py
