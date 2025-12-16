import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    // Mock response - replace with actual backend API call
    const mockResponse = {
      servers: [
        {
          id: "weather-agent-001",
          name: "Weather Agent",
          url: "https://weather-agent.example.com",
          description:
            "Provides current weather conditions, forecasts, and historical weather data for locations worldwide.",
          isHealthy: true,
          metadata: {
            category: "Weather",
            costPerCall: 0.002,
          },
          tools: [
            { name: "getCurrentWeather", description: "Get current weather for a location" },
            { name: "getForecast", description: "Get weather forecast for the next 7 days" },
          ],
        },
        {
          id: "finance-agent-001",
          name: "Finance Agent",
          url: "https://finance-agent.example.com",
          description:
            "Retrieves real-time stock prices, market data, financial news, and performs basic financial calculations.",
          isHealthy: true,
          metadata: {
            category: "Finance",
            costPerCall: 0.003,
          },
          tools: [
            { name: "getStockPrice", description: "Get current stock price" },
            { name: "getMarketData", description: "Get market overview" },
          ],
        },
        {
          id: "translation-agent-001",
          name: "Translation Agent",
          url: "https://translation-agent.example.com",
          description:
            "Provides high-quality language translation services supporting over 100 languages with context awareness.",
          isHealthy: false,
          metadata: {
            category: "Language",
            costPerCall: 0.001,
          },
          tools: [
            { name: "translateText", description: "Translate text between languages" },
            { name: "detectLanguage", description: "Detect the language of text" },
          ],
        },
      ],
    }

    return NextResponse.json(mockResponse)
  } catch (error) {
    return NextResponse.json({ error: "Failed to fetch servers" }, { status: 500 })
  }
}
