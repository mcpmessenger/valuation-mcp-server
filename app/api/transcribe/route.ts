import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const audioFile = formData.get("file") as File

    if (!audioFile) {
      return NextResponse.json({ error: "No audio file provided" }, { status: 400 })
    }

    // Mock transcription response - In production, integrate with OpenAI Whisper API
    // const openaiFormData = new FormData()
    // openaiFormData.append("file", audioFile)
    // openaiFormData.append("model", "whisper-1")
    //
    // const response = await fetch("https://api.openai.com/v1/audio/transcriptions", {
    //   method: "POST",
    //   headers: {
    //     Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
    //   },
    //   body: openaiFormData,
    // })
    // const { text } = await response.json()

    // Mock response for demo purposes
    await new Promise((resolve) => setTimeout(resolve, 1000))
    const text = "What's the weather in San Francisco?"

    return NextResponse.json({ text })
  } catch (error) {
    console.error("[v0] Transcription error:", error)
    return NextResponse.json({ error: "Failed to transcribe audio" }, { status: 500 })
  }
}
