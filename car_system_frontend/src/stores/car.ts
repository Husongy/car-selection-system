import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Car } from '@/types/car'

export const useCarStore = defineStore('car', () => {
  const selectedCar = ref<Car | null>(null)
  const favoriteList = ref<Car[]>([])

  // 设置选中的车辆
  const setSelectedCar = (car: Car) => {
    selectedCar.value = car
  }

  // 添加到收藏
  const addToFavorite = (car: Car) => {
    const index = favoriteList.value.findIndex(item => item.id === car.id)
    if (index === -1) {
      favoriteList.value.push(car)
      saveFavoriteToLocal()
    }
  }

  // 从收藏中移除
  const removeFromFavorite = (carId: number) => {
    const index = favoriteList.value.findIndex(item => item.id === carId)
    if (index > -1) {
      favoriteList.value.splice(index, 1)
      saveFavoriteToLocal()
    }
  }

  // 保存收藏到本地
  const saveFavoriteToLocal = () => {
    localStorage.setItem('favoriteCars', JSON.stringify(favoriteList.value))
  }

  // 从本地加载收藏
  const loadFavoriteFromLocal = () => {
    const saved = localStorage.getItem('favoriteCars')
    if (saved) {
      try {
        favoriteList.value = JSON.parse(saved)
      } catch (error) {
        console.error('加载收藏列表失败:', error)
      }
    }
  }

  return {
    selectedCar,
    favoriteList,
    setSelectedCar,
    addToFavorite,
    removeFromFavorite,
    loadFavoriteFromLocal
  }
})
