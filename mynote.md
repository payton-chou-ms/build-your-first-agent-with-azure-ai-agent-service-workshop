# 業務場景總覽說明
本專案包含多個範例與練習，分為「單一代理」與「多代理」兩大類，以及其他相關服務整合
包含了 Azure AI Agent Service 與 AI Search、TimeGen 模型、PostgreSQL DB、AutoGen Framework、Semantic Kernel Framework 與 Model Context Protocol (MCP) 的整合範例
並且設計各種業務場景，讓使用者能夠透過自然語言查詢、資料分析、視覺化報告等功能，提升工作效率與決策能力

## **建置第一個 Agent（Workshop）**  
透過可視化與資料匯出，整合我們與主要競品在各區域的入門級帳篷型號與價格，以支持快速決策與自動化報表
### Function Calling 範例
- 按地區劃分的銷售額是多少？
- 上個季度的收入是多少？
- 哪些產品在歐洲賣得最好？
- 按地區劃分的總運費？
- 顯示最近的 3 筆交易詳細資訊
- 按類別顯示歐洲的銷售額
- 按鞋類劃分的突破銷售額

### PDF 相關查詢
- 我們銷售哪些品牌的登山鞋？
- 我們銷售哪些品牌的帳篷？
- 這些品牌與哪些商品類型和分類相關聯？
- 2024 年按產品類型劃分的帳篷銷量是多少？包括與每個品牌關聯的品牌。
- Contoso 不銷售 AlpineGear 的家庭露營帳篷

### Code Interpreter 相關查詢
- 以餅圖的形式按區域顯示銷售額
- 下載按地區劃分的銷售額數據
- 下載為 JSON 格式

### Bing Search 相關查詢
- 我們的競爭對手銷售哪些初學者帳篷？包括價格。

### 多語言可視化
- 查詢 2022 年各區域銷售額
  - 回傳結果使用韓文
  - 以餅圖顯示

### 綜合查詢範例
- 我們銷售哪些新手帳篷？
  - **Note**: 這些資訊主要來自我們在 vector 資訊存儲中提供的檔。
- 我們的競爭對手銷售哪些新手帳篷？價格如何？
  - **Note**: 此資訊來自 Internet，包括實際產品名稱和價格。
- 顯示為直條圖
  - **Note**: AI Agent Service 再次使用 Code Interpreter 建立圖表，但這次使用來自上一個查詢中的真實數據。
- 請列出依照不同地區展示所銷售的帳篷，其售價與市場競爭對手的入門級帳篷相近
  - **Note**: 此查詢依賴於基礎大型語言模型的推理功能，以及函數調用返回的數據。
- 將數據下載為人類可讀的 JSON 檔
  - **Note**: 此查詢再次依賴於 Code Interpreter 從以前的查詢。

## **Azure AI Agent Service 與 AI Search 整合**
透過 AI 搜尋代理即時提供心臟病衛教單、生活方式及醫療管理建議，以及症狀與預防措施資訊
- 請給我心臟病衛教單
- 心臟病患者在生活方式和醫療管理方面的建議
- 心臟病的症狀和預防措施
## **Azure AI Agent Service 與 TimeGen 模型整合**
利用結構化資料進行網路安全異常偵測與趨勢預測，並結合 Timegen Model 產出視覺化分析結果，協助安全決策
## **Azure AI Agent Service 與 PostgreSQL DB 整合**
打造一個能以自然語言接收法律查詢、透過向量搜尋檢索判例並分析總結結果，以支援華盛頓州法律團隊研究的智慧代理
## AutoGen Framework 與 AI Agent Service 整合
透過規劃代理人將網絡安全報告生成流程拆解為時間管理、資料收集、資料庫讀取、數據分析、指標評估與報告撰寫等子任務，並分派給對應專屬代理以高效協作完成整體報告
## Semantic Kernel Framework 與 AI Agent Service 整合
利用 Azure OpenAI／OpenAI 建立帶有專屬角色指令（ArtDirector 與 CopyWriter）的聊天代理，並讓它們在群組對話中協同滿足使用者需求
## Model Context Protocol (MCP) framework integrate with AI Agent Service
透過 VS Code 中的 GitHub Copilot，並結合 MCP 協議，即時查詢並滿足專案文件需求以提升開發效率
### my-project-agent 專案問題清單
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

# 專案結構總覽

本專案包含多個範例與練習，分為「單一代理」與「多代理」兩大類，以及其他相關工具和測試程式

---

## 單一代理（Single Agent）練習

### **建置第一個 Agent（Workshop）**
- **功能**：整合我們與主要競品在各區域的入門級帳篷型號與價格，支持快速決策與自動化報表。
- **路徑**：`src/python/workshop/main.py`

### **Azure AI Agent Service 與 AI Search 整合**
- **功能**：即時提供心臟病衛教單、生活方式建議及症狀與預防措施資訊。
- **路徑**：`src/python/workshop/my-ai-search-agent.py`

### **Azure AI Agent Service 與 TimeGen 模型整合**
- **功能**：進行網路安全異常偵測與趨勢預測，並產出視覺化分析結果。
- **路徑**：`src/python/workshop/timegen/data_analyzer.ipynb`

### **Azure AI Agent Service 與 PostgreSQL DB 整合**
- **功能**：以自然語言接收法律查詢，檢索判例並分析總結結果，支援法律研究。
- **路徑**：
  - `src/python/workshop/postgres-agent/src/simple_postgres_and_ai_agent.py`
  - `src/python/workshop/postgres-agent/src/advanced_postgres_and_ai_agent_with_tracing.py`

---

## 多代理（Multi Agent）練習

### **AutoGen Framework 與 AI Agent Service 整合**
- **功能**：將網絡安全報告生成流程拆解為多個子任務，並分派給專屬代理高效協作完成。
- **路徑**：
  - 設定與範例程式：`src/python/workshop/autogen/00_set_up`
  - 進階群組聊天安全範例：`src/python/workshop/autogen/06_cyber_security_group_chat.ipynb`

### **Semantic Kernel Framework 與 AI Agent Service 整合**
- **功能**：建立帶有專屬角色指令（如 ArtDirector 和 CopyWriter）的聊天代理，協同滿足使用者需求。
- **範例程式**：
  - `src/python/workshop/azure_ai_agent (sk)/step1_azure_ai_agent.py`
  - `src/python/workshop/azure_ai_agent (sk)/step2_azure_ai_agent_plugin.py`
  - `src/python/workshop/azure_ai_agent (sk)/step3_azure_ai_agent_group_chat.py`
  - `src/python/workshop/azure_ai_agent (sk)/step4_azure_ai_agent_code_interpreter.py`
  - `src/python/workshop/azure_ai_agent (sk)/step5_azure_ai_agent_file_search.py`
  - `src/python/workshop/azure_ai_agent (sk)/step6_azure_ai_agent_openapi.py`
  - `src/python/workshop/azure_ai_agent (sk)/step7_azure_ai_agent_retrieval.py`

### **Model Context Protocol (MCP) Framework 與 AI Agent Service 整合**
- **功能**：結合 MCP 協議，即時查詢並滿足專案文件需求以提升開發效率。
- **路徑**：
  - `src/python/workshop/mcp/azure_agent_mcp_server/__main__.py`
  - `src/python/workshop/mcp/my-project-agent.py`




# 專案技術細節
## **建置第一個 Agent（Workshop）**  
- Doc
  README.md
  [Contoso Sales AI Agent](https://aka.ms/agent-service-workshop-docs).
## **Azure AI Agent Service 與 AI Search 整合**
- Doc
  - To ADD
## **Azure AI Agent Service 與 TimeGen 模型整合**
- Doc
  - To ADD
## **Azure AI Agent Service 與 PostgreSQL DB 整合**
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

## AutoGen Framework 與 AI Agent Service 整合
- Doc
  - In jupyter notebook code
## Semantic Kernel Framework 與 AI Agent Service 整合
- Check src/python/workshop/azure_ai_agent (sk)/README.md for more details
## Model Context Protocol (MCP) framework integrate with AI Agent Service
# Azure Agent MCP Server
## 注意事項
請更新.env的內容, 把這agent設定正確
<pre>
# Azure AI Agent Service connection string
PROJECT_CONNECTION_STRING="eastus2.api.azureml.ms;846817e9-ac19-4006-9827-a125xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Default agent ID
DEFAULT_AGENT_ID="asst_DVWlHohxxxxxxxxxxxxxxxxx" # Project Spec Agent
</pre>

## Local Test
$ cd src/python/azure_agent_mcp_server/
$ python __main__.py


## VS code 設定 (setting.json)
    "mcp": {
        "servers": {
            "my-mcp-server-project-spec-agent": {
                "type": "stdio",
                "command": "C:\\Users\\chihengchou\\Downloads\\work\\work\\mcp-foundry\\.venv\\Scripts\\python.exe",
                "_command": "python",
                "args": [
                    "/Users/chihengchou/Downloads/work/work/build-your-first-agent-with-azure-ai-agent-service-workshop/src/python/workshop/mcp/azure_agent_mcp_server/__main__.py"
                ]
            }
        }
    }

#                    "/Users/chihengchou/Downloads/work/work/mcp-foundry/src/python/azure_agent_mcp_server/__main__.py"

## 在 VS code 中使用
- 請在Copilot Chat中選擇 agent mode
- 點選工具圖示, 確認使用的工具是哪個
- 或是使用 Hashtag query_default_agent, 就可以指定使用自己的agent
- 或是使用list_agent, 就可以列出所有的agent, 然後再使用connect_agent, 來連接到指定的agent

- python my-project-agent.py
