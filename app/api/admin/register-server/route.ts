import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { id, name, url, description, category, costPerCall } = body

    // Mock response - replace with actual backend API call
    console.log("[v0] Registering server:", { id, name, url, description, category, costPerCall })

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    return NextResponse.json({
      success: true,
      message: "Server registered successfully",
    })
  } catch (error) {
    return NextResponse.json({ error: "Failed to register server" }, { status: 500 })
  }
}
