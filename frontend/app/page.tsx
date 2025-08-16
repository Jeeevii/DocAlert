"use client"

import type React from "react"

import { useState } from "react"
import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import {
  Upload,
  FileText,
  Shield,
  Bell,
  Clock,
  ArrowRight,
  CheckCircle,
  XCircle,
  Menu,
  Send,
  Bot,
  Loader2,
} from "lucide-react"

export default function ParserateLanding() {
  const [dragActive, setDragActive] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [email, setEmail] = useState("")
  const [phone, setPhone] = useState("")
  const [documentType, setDocumentType] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    const files = e.dataTransfer.files
    if (files && files[0]) {
      setUploadedFile(files[0])
    }
  }

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files[0]) {
      setUploadedFile(files[0])
    }
  }

  const handleParseDocument = async () => {
    if (!uploadedFile || !email || !documentType) {
      alert("Please fill in all required fields and upload a document")
      return
    }

    setIsProcessing(true)

    // Simulate processing time
    await new Promise((resolve) => setTimeout(resolve, 3000))

    setIsProcessing(false)
    setShowResults(true)

    // Scroll to results
    setTimeout(() => {
      document.getElementById("results-section")?.scrollIntoView({ behavior: "smooth" })
    }, 100)
  }

  const scrollToDemo = () => {
    document.getElementById("demo-section")?.scrollIntoView({ behavior: "smooth" })
  }

  const scrollToHowItWorks = () => {
    document.getElementById("how-it-works")?.scrollIntoView({ behavior: "smooth" })
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header/Nav with logo and navigation links */}
      <header className="px-4 py-4 sm:px-6 lg:px-8 bg-white border-b border-gray-100">
        <div className="mx-auto max-w-7xl flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <motion.div
              animate={{ rotate: [0, 5, -5, 0] }}
              transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY, repeatDelay: 3 }}
              className="w-10 h-10 bg-gradient-to-br from-teal-500 to-indigo-600 rounded-xl flex items-center justify-center"
            >
              <Send className="w-6 h-6 text-white" />
            </motion.div>
            <span className="text-2xl font-bold text-slate-800">Parserate</span>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-slate-600 hover:text-slate-800 font-medium transition-colors">
              Features
            </a>
            <a href="#how-it-works" className="text-slate-600 hover:text-slate-800 font-medium transition-colors">
              How It Works
            </a>
            <a href="#docs" className="text-slate-600 hover:text-slate-800 font-medium transition-colors">
              Docs
            </a>
            <a href="#contact" className="text-slate-600 hover:text-slate-800 font-medium transition-colors">
              Contact
            </a>
            <Button onClick={scrollToDemo} className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2 rounded-lg">
              Try Parserate Free
            </Button>
          </nav>

          <Button variant="ghost" size="sm" className="md:hidden">
            <Menu className="w-6 h-6" />
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative px-4 py-20 sm:px-6 lg:px-8 bg-gradient-to-br from-teal-500 via-teal-600 to-indigo-600 text-white overflow-hidden"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-teal-500/90 via-teal-600/90 to-indigo-600/90" />

        <div className="relative mx-auto max-w-5xl">
          <div className="text-center">
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 3, repeat: Number.POSITIVE_INFINITY }}
              className="mx-auto w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center mb-8"
            >
              <Send className="w-10 h-10 text-white" />
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.8 }}
              className="text-5xl font-bold tracking-tight sm:text-7xl mb-8"
            >
              Skip the paperwork ping-pong.
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.8 }}
              className="mt-6 text-xl sm:text-2xl text-teal-50 max-w-4xl mx-auto leading-relaxed"
            >
              Parserate validates user data before humans ever touch it. Extracts, checks, and flags issues
              automatically — so your team only handles clean, verified documents.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="mt-10 flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Button
                onClick={scrollToDemo}
                size="lg"
                className="bg-white text-teal-600 hover:bg-gray-50 px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
              >
                Get Started
              </Button>
              <Button
                onClick={scrollToHowItWorks}
                variant="outline"
                size="lg"
                className="border-white text-white hover:bg-white hover:text-teal-600 px-8 py-4 text-lg font-semibold rounded-xl transition-all duration-300 bg-transparent"
              >
                See How It Works
              </Button>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Fun Fact / Data Insight Section with 40% stat */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        className="px-4 py-16 sm:px-6 lg:px-8 bg-white"
      >
        <div className="mx-auto max-w-4xl">
          <Card className="rounded-3xl shadow-2xl border-0 bg-gradient-to-br from-amber-50 to-orange-50 overflow-hidden">
            <CardContent className="p-12 text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-8">
                <Clock className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-6xl font-bold text-slate-800 mb-4">40%</h2>
              <p className="text-2xl font-semibold text-slate-700 mb-6">
                of work hours are wasted on document verification.
              </p>
              <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto">
                Most businesses spend days going back and forth fixing small data errors. Parserate prevents mistakes
                before they reach your team.
              </p>
              <div className="bg-white rounded-2xl p-6 shadow-lg">
                <p className="text-xl font-bold text-amber-600">We cut the process down from days to minutes.</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </motion.section>

      {/* Time-Saving Callout section */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        className="px-4 py-16 sm:px-6 lg:px-8 bg-gray-50"
      >
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-5xl font-bold text-slate-800 mb-4">Save 3–5 days per workflow</h2>
          <p className="text-2xl text-slate-600">No more endless back-and-forth corrections.</p>
        </div>
      </motion.section>

      {/* Visual Workflow Timeline Graphic */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        id="how-it-works"
        className="px-4 py-20 sm:px-6 lg:px-8 bg-white"
      >
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold text-slate-800 mb-4">Visual Workflow</h3>
            <p className="text-xl text-slate-600">From upload to validation in seconds</p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            <motion.div whileHover={{ scale: 1.05 }} className="text-center relative">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <Upload className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-lg font-bold text-slate-800 mb-2">1. User uploads document</h4>
              <p className="text-slate-600">Drag & drop any file type</p>
              <div className="hidden md:block absolute top-8 -right-4 text-slate-300">
                <ArrowRight className="w-6 h-6" />
              </div>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="text-center relative">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-400 to-teal-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <Bot className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-lg font-bold text-slate-800 mb-2">2. Parserate parses + validates automatically</h4>
              <p className="text-slate-600">AI extracts and checks data</p>
              <div className="hidden md:block absolute top-8 -right-4 text-slate-300">
                <ArrowRight className="w-6 h-6" />
              </div>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="text-center relative">
              <div className="w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <Bell className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-lg font-bold text-slate-800 mb-2">3. Issues flagged instantly</h4>
              <p className="text-slate-600">SMS/Email alerts sent</p>
              <div className="hidden md:block absolute top-8 -right-4 text-slate-300">
                <ArrowRight className="w-6 h-6" />
              </div>
            </motion.div>

            <motion.div whileHover={{ scale: 1.05 }} className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-lg font-bold text-slate-800 mb-2">4. Human only reviews clean, valid files</h4>
              <p className="text-slate-600">No more messy documents</p>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Feature Highlights */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        id="features"
        className="px-4 py-20 sm:px-6 lg:px-8 bg-gray-50"
      >
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-800 mb-4">Powerful Features</h2>
            <p className="text-xl text-slate-600">Everything you need for reliable document processing</p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            <motion.div whileHover={{ y: -8, scale: 1.02 }} transition={{ duration: 0.3 }}>
              <Card className="rounded-2xl shadow-lg border-0 bg-white hover:shadow-2xl transition-all duration-300 h-full">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-br from-teal-400 to-teal-600 rounded-2xl flex items-center justify-center mb-6">
                    <FileText className="w-8 h-8 text-white" />
                  </div>
                  <CardTitle className="text-slate-800 text-xl">AI Parsing</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <CardDescription className="text-slate-600 text-base">
                    Handles PDFs, scans, text files & more
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div whileHover={{ y: -8, scale: 1.02 }} transition={{ duration: 0.3 }}>
              <Card className="rounded-2xl shadow-lg border-0 bg-white hover:shadow-2xl transition-all duration-300 h-full">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-br from-indigo-400 to-indigo-600 rounded-2xl flex items-center justify-center mb-6">
                    <Shield className="w-8 h-8 text-white" />
                  </div>
                  <CardTitle className="text-slate-800 text-xl">Validation Engine</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <CardDescription className="text-slate-600 text-base">
                    Strict rules catch errors early
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div whileHover={{ y: -8, scale: 1.02 }} transition={{ duration: 0.3 }}>
              <Card className="rounded-2xl shadow-lg border-0 bg-white hover:shadow-2xl transition-all duration-300 h-full">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl flex items-center justify-center mb-6">
                    <Bot className="w-8 h-8 text-white" />
                  </div>
                  <CardTitle className="text-slate-800 text-xl">AI Phone Calls</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <CardDescription className="text-slate-600 text-base">
                    Automated agents call users for missing info
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>

            <motion.div whileHover={{ y: -8, scale: 1.02 }} transition={{ duration: 0.3 }}>
              <Card className="rounded-2xl shadow-lg border-0 bg-white hover:shadow-2xl transition-all duration-300 h-full">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-16 h-16 bg-gradient-to-br from-amber-400 to-pink-500 rounded-2xl flex items-center justify-center mb-6">
                    <Bell className="w-8 h-8 text-white" />
                  </div>
                  <CardTitle className="text-slate-800 text-xl">Real-time Alerts</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <CardDescription className="text-slate-600 text-base">
                    Instantly notify users of issues
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </motion.section>

      {/* Main Input Section */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
        id="demo-section"
        className="px-4 py-20 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-50 to-gray-100"
      >
        <div className="mx-auto max-w-3xl">
          <div className="text-center mb-12">
            <h3 className="text-4xl font-bold text-slate-800 mb-4">Try It Now</h3>
            <p className="text-xl text-slate-600">See Parserate in action with your documents</p>
          </div>

          <Card className="rounded-3xl shadow-2xl border-0 bg-white overflow-hidden">
            <CardContent className="p-10 space-y-10">
              {/* File Upload Area */}
              <div
                className={`border-2 border-dashed rounded-2xl p-16 text-center transition-all duration-300 cursor-pointer ${
                  dragActive
                    ? "border-teal-400 bg-gradient-to-br from-teal-50 to-indigo-50 scale-105"
                    : "border-slate-300 hover:border-teal-400 hover:bg-gradient-to-br hover:from-teal-50 hover:to-indigo-50"
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById("file-input")?.click()}
              >
                <input
                  id="file-input"
                  type="file"
                  className="hidden"
                  accept=".pdf,.txt,.doc,.docx,.png,.jpg,.jpeg"
                  onChange={handleFileInput}
                />

                {uploadedFile ? (
                  <div>
                    <CheckCircle className="mx-auto h-16 w-16 text-green-500 mb-6" />
                    <p className="text-slate-700 mb-2 text-lg font-semibold">{uploadedFile.name}</p>
                    <p className="text-slate-500">{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                    <Button
                      variant="outline"
                      className="mt-4 bg-transparent"
                      onClick={(e) => {
                        e.stopPropagation()
                        setUploadedFile(null)
                      }}
                    >
                      Remove File
                    </Button>
                  </div>
                ) : (
                  <div>
                    <Upload className="mx-auto h-16 w-16 text-slate-400 mb-6" />
                    <p className="text-slate-700 mb-2 text-lg">
                      <span className="font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-slate-500">PDF, TXT, DOC, DOCX, PNG, JPG, scanned images up to 10MB</p>
                  </div>
                )}
              </div>

              {/* Form Fields */}
              <div className="grid gap-8 md:grid-cols-2">
                <div className="space-y-4">
                  <Label htmlFor="email" className="text-slate-700 font-medium text-base">
                    Email *
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="rounded-xl border-slate-300 focus:border-teal-500 focus:ring-teal-500 h-14 bg-slate-50 focus:bg-white transition-colors"
                  />
                </div>
                <div className="space-y-4">
                  <Label htmlFor="phone" className="text-slate-700 font-medium text-base">
                    Phone Number
                  </Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+1 (555) 123-4567"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="rounded-xl border-slate-300 focus:border-teal-500 focus:ring-teal-500 h-14 bg-slate-50 focus:bg-white transition-colors"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <Label htmlFor="document-type" className="text-slate-700 font-medium text-base">
                  Document Type *
                </Label>
                <Select value={documentType} onValueChange={setDocumentType}>
                  <SelectTrigger className="rounded-xl border-slate-300 focus:border-teal-500 focus:ring-teal-500 h-14 bg-slate-50 focus:bg-white transition-colors">
                    <SelectValue placeholder="Select document type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="w4">W-4 Tax Form</SelectItem>
                    <SelectItem value="i9">I-9 Employment Form</SelectItem>
                    <SelectItem value="passport">Passport</SelectItem>
                    <SelectItem value="drivers-license">Driver's License</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button
                onClick={handleParseDocument}
                disabled={isProcessing || !uploadedFile || !email || !documentType}
                className="w-full bg-gradient-to-r from-teal-600 to-indigo-600 hover:from-teal-700 hover:to-indigo-700 text-white py-5 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 text-lg font-semibold hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                size="lg"
              >
                {isProcessing ? (
                  <div className="flex items-center justify-center">
                    <Loader2 className="w-6 h-6 animate-spin mr-3" />
                    Processing Document...
                  </div>
                ) : (
                  "Parse Document"
                )}
              </Button>
            </CardContent>
          </Card>
        </div>
      </motion.section>

      {showResults && (
        <motion.section
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          id="results-section"
          className="px-4 py-16 sm:px-6 lg:px-8 bg-white"
        >
          <div className="mx-auto max-w-2xl">
            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold text-slate-800 mb-2">Processing Complete!</h3>
              <p className="text-slate-600">Here are your validation results</p>
            </div>

            <div className="space-y-4">
              <Card className="rounded-2xl shadow-lg border-0 bg-white">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="font-semibold text-slate-800">Document: {uploadedFile?.name}</h4>
                      <p className="text-sm text-slate-600">Type: {documentType.toUpperCase()}</p>
                      <p className="text-sm text-slate-600">Processed just now</p>
                    </div>
                    <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                      <CheckCircle className="w-4 h-4 mr-1" />
                      Valid
                    </Badge>
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm text-slate-600">✓ All required fields present and validated</p>
                    <p className="text-sm text-slate-600">✓ Email format verified: {email}</p>
                    {phone && <p className="text-sm text-slate-600">✓ Phone number format validated: {phone}</p>}
                    <p className="text-sm text-slate-600">✓ Document type matches content</p>
                  </div>
                </CardContent>
              </Card>

              <div className="text-center pt-6">
                <Button
                  onClick={() => {
                    setShowResults(false)
                    setUploadedFile(null)
                    setEmail("")
                    setPhone("")
                    setDocumentType("")
                  }}
                  variant="outline"
                  className="mr-4"
                >
                  Process Another Document
                </Button>
                <Button className="bg-teal-600 hover:bg-teal-700 text-white">Download Results</Button>
              </div>
            </div>
          </div>
        </motion.section>
      )}

      {/* Validation Result Preview - Only show when not showing actual results */}
      {!showResults && (
        <motion.section
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="px-4 py-16 sm:px-6 lg:px-8 bg-white"
        >
          <div className="mx-auto max-w-2xl">
            <div className="text-center mb-8">
              <h3 className="text-2xl font-bold text-slate-800 mb-2">Validation Results</h3>
              <p className="text-slate-600">See what Parserate delivers</p>
            </div>

            <div className="space-y-4">
              <Card className="rounded-2xl shadow-sm border-0 bg-white">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="font-semibold text-slate-800">Document Type: W-4</h4>
                      <p className="text-sm text-slate-600">Processed 2 seconds ago</p>
                    </div>
                    <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                      <CheckCircle className="w-4 h-4 mr-1" />
                      Valid
                    </Badge>
                  </div>
                  <p className="text-sm text-slate-600">All required fields present and validated</p>
                </CardContent>
              </Card>

              <Card className="rounded-2xl shadow-sm border-0 bg-white">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="font-semibold text-slate-800">Document Type: I-9</h4>
                      <p className="text-sm text-slate-600">Processed 5 seconds ago</p>
                    </div>
                    <Badge className="bg-red-100 text-red-800 hover:bg-red-100">
                      <XCircle className="w-4 h-4 mr-1" />
                      Invalid
                    </Badge>
                  </div>
                  <p className="text-sm text-slate-600">Notes: Missing SSN field</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </motion.section>
      )}

      {/* Footer */}
      <footer className="px-4 py-12 sm:px-6 lg:px-8 bg-slate-900 text-white">
        <div className="mx-auto max-w-4xl">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="mb-6 md:mb-0 flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-indigo-600 rounded-xl flex items-center justify-center">
                <Send className="w-6 h-6 text-white" />
              </div>
              <div>
                <h4 className="text-2xl font-bold text-white mb-1">Parserate</h4>
                <p className="text-slate-400">© 2025 Parserate</p>
              </div>
            </div>
            <div className="flex space-x-8">
              <a href="#docs" className="text-slate-400 hover:text-white transition-colors font-medium">
                Docs
              </a>
              <a href="#contact" className="text-slate-400 hover:text-white transition-colors font-medium">
                Contact
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors font-medium">
                GitHub
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
