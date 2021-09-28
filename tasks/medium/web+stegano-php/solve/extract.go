package main

import (
	"image"
	"image/color"
	_ "image/png"
	"os"
)

func NewByteBuilder() *ByteBuilder {
	return &ByteBuilder{state: 0, pos: 7}
}

type ByteBuilder struct {
	state uint8
	pos   int
}

// Filled or no.
func (bb *ByteBuilder) Add(bit uint8) bool {
	bb.state |= (bit << bb.pos)
	bb.pos -= 1
	return bb.pos == -1
}

func (bb *ByteBuilder) Build() byte {
	return bb.state
}

func (bb *ByteBuilder) Clear() {
	bb.state = 0
	bb.pos = 7
}

type BitExtractor struct {
	channel  string
	position int
}

func extractBit(config BitExtractor, c color.Color) uint8 {
	r, g, b, a := c.RGBA()
	config.position -= 1
	var val uint8
	if config.channel == "r" {
		val = uint8(r >> 8)
	}
	if config.channel == "g" {
		val = uint8(g >> 8)
	}
	if config.channel == "b" {
		val = uint8(b >> 8)
	}
	if config.channel == "a" {
		val = uint8(a >> 8)
	}
	return (val & (1 << config.position)) >> uint8(config.position)
}

func main() {
	imageInput := os.Args[1]

	pngFile, err := os.Open(imageInput)
	if err != nil {
		// replace this with real error handling
		panic(err)
	}
	defer pngFile.Close()
	pngImg, _, err := image.Decode(pngFile)
	if err != nil {
		// replace this with real error handling
		panic(err)
	}

	extractors := []BitExtractor{
		{"r", 1}, {"r", 2}, {"b", 1}, {"b", 2},
	}

	bb := NewByteBuilder()
	var out []byte
	bounds := pngImg.Bounds()
	w, h := bounds.Max.X, bounds.Max.Y

	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			c := pngImg.At(x, y)
			for _, e := range extractors {
				eb := extractBit(e, c)
				if bb.Add(eb) {
					out = append(out, bb.Build())
					bb.Clear()
				}
			}
		}
	}

	os.Stdout.Write(out)
}
