import Head from 'next/head'
import styles from '../styles/Home.module.css'
import Input from '../components/Input'
import Button from '../components/Button'
import Title from '../components/Title'

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center min-h-screen py-2 gap-3">
      <Title />
      <div className="flex flex-row gap-3">
        <Input />
      </div>
    </main>
  )
}