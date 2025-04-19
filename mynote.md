az login --tenant 16b3c013-d300-468d-ac64-7eda0820b6d3

# command
cd src/python/workshop
python main.py

# main.py
## Questions for Function calling
按地區劃分的銷售額是多少？
上個季度的收入是多少？
哪些產品在歐洲賣得最好？
按地區劃分的總運費？
顯示最近的 3 筆交易詳細資訊
按類別顯示歐洲的銷售額
按鞋類劃分的突破銷售額
## Questions for PDF
我們銷售哪些品牌的登山鞋？
我們銷售哪些品牌的帳篷？
這些品牌與哪些商品類型和分類相關聯？
2024年按產品類型劃分的帳篷銷量是多少？包括與每個品牌關聯的品牌。
Contoso 不銷售 AlpineGear 的家庭露營帳篷
## Questions for Code Interpreter
以餅圖的形式按區域顯示銷售額
下載按地區劃分的銷售額數據
下載為 JSON 格式
## Questions for Bing Search
我們的競爭對手銷售哪些初學者帳篷？包括價格。
## ## 多語言可視化
What were the sales by region for 2022
In Korean
Show as a pie chart

## Questions for all
- 我們銷售哪些新手帳篷？
  note: 這些資訊主要來自我們在 vector 資訊存儲中提供的檔。
- 我們的競爭對手銷售哪些新手帳篷？價格如何？
  note: 此資訊來自 Internet，包括實際產品名稱和價格。
- 顯示為直條圖
  note: AI Agent Service 再次使用 Code Interpreter 建立圖表，但這次使用 來自上一個查詢中的真實數據。和以前一樣，查看圖表。src/workshop/files
- 請列出依照不同地區展示所銷售的帳篷，其售價與市場競爭對手的入門級帳篷相近
  note: 此查詢依賴於基礎大型語言模型的推理功能，以及函數調用返回的數據
- 將數據下載為人類可讀的 JSON 檔
  note: 此查詢再次依賴於 Code Interpreter 從 以前的查詢

# my-project-agent
- Questions for project:

1. 在智能家居控制中心規格書中, 如何使用登入 API 來驗證用戶身份？
2. 在智能家居控制中心規格書中, 如何下發一個控制指令來調整設備亮度？
3. 在智能家居控制中心規格書中, 系統如何確保 API 請求的安全性？
4. 在智能家居控制中心規格書中, 如何查詢設備日誌記錄，並且可以使用哪些查詢參數？
5. 在智能家居控制中心規格書中, 當 API 請求缺少必要參數時，系統會返回什麼錯誤資訊？
6. 在智能家居控制中心規格書中, 新用戶如何使用註冊 API 創建帳戶？
7. 在智能家居控制中心規格書中, 什麼是設備發現 API，其主要用途是什麼？
8. 在智能家居控制中心規格書中, 情景模式 API 如何協助實現多設備協同控制？
9. 在智能家居控制中心規格書中, 在 API 文件中如何進行版本管理？
10. 在智能家居控制中心規格書中, API 回應格式通常包括哪些關鍵字段？
11. 在智能家居控制中心規格書中,如何描述安全性與通訊加密?
12. 在智能家居控制中心規格書中,查詢操作日誌包含?


# my-ai-search-agent

- Questions for AI Search Agent:
  - 請給我心臟病衛教單
  - 心臟病患者在生活方式和醫療管理方面的建議
  - 心臟病的症狀和預防措施

# Semantic Kernel
- Check src/python/workshop/azure_ai_agent/README.md for more details

# Postgres Agent
- Check src/python/workshop/postgres_agent/README.md for more details
- Setup steps:
  - Create a new Azure Database for PostgreSQL flexible server in Azure Portal
  - Enable the vector and azure_ai extensions in Settings > Server parameters > azure.extensions
  - Make sure firewall rules are set to allow access from your IP address
    - Settings > Connect > pre-requisites check
  - Test the connection using pgAdmin
    - Download postgresql from https://www.postgresql.org/download/windows/
    - Launch pgAdmin 4 and create a new server connection
    - Check if postgres db is accessible and the vector and azure_ai extensions are installed
    - Test the connection using the following command:
      select azure_ai.version();
      SELECT azure_ai.get_setting('azure_openai.subscription_key')
      SELECT azure_ai.get_setting('azure_openai.endpoint')
- Run
  - To load data into the database, run the following commands in the terminal:
    - cd src/python/workshop/postgres_agent/load_data
    - python main.py
  - To run the AI agent, run the following commands in the terminal:
    - cd src/python/workshop/postgres_agent/src
    - python simple_postgres_and_ai_agent.py
  - To run the AI agent with tracing, run the following commands in the terminal:
    - cd src/python/workshop/postgres_agent/src  
    - python advanced_postgres_and_ai_agent_with_tracing.py