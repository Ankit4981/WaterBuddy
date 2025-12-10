import React, { useState, useEffect } from 'react';
import { Droplets, User, Settings, RotateCcw, Plus, Target, TrendingUp } from 'lucide-react';

const WaterBuddyApp = () => {
  const [screen, setScreen] = useState('welcome');
  const [name, setName] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [gender, setGender] = useState('');
  const [weight, setWeight] = useState('70');
  const [unit, setUnit] = useState('kg');
  const [dailyGoal, setDailyGoal] = useState(2700);
  const [totalIntake, setTotalIntake] = useState(0);
  const [customAmount, setCustomAmount] = useState('250');

  const ageGroups = {
    'Kids (4-8 years)': { goal: 1200, emoji: '👶' },
    'Teens (9-13 years)': { goal: 1700, emoji: '🧒' },
    'Adults (14-64 years)': { goal: 2000, emoji: '🧑' },
    'Seniors (65+ years)': { goal: 1800, emoji: '👴' }
  };

  useEffect(() => {
    if (ageGroup) {
      const baseGoal = ageGroups[ageGroup].goal;
      const weightNum = parseFloat(weight);
      const adjustedGoal = Math.round(baseGoal + (weightNum * 10));
      setDailyGoal(adjustedGoal);
    }
  }, [ageGroup, weight]);

  const percentage = Math.min((totalIntake / dailyGoal) * 100, 100);
  const remaining = Math.max(dailyGoal - totalIntake, 0);

  const addWater = (amount) => {
    setTotalIntake(prev => prev + amount);
  };

  const resetIntake = () => {
    setTotalIntake(0);
  };

  const getDroppyMessage = () => {
    if (percentage >= 100) return { text: "🎉 Goal Achieved! Amazing!", color: "text-green-600" };
    if (percentage >= 75) return { text: "💪 Keep it up! Almost there!", color: "text-blue-600" };
    if (percentage >= 50) return { text: "👍 Great progress! Stay hydrated!", color: "text-cyan-600" };
    return { text: "💧 Let's stay hydrated! Small sips add up", color: "text-sky-600" };
  };

  const message = getDroppyMessage();

  // Welcome Screen
  if (screen === 'welcome') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full text-center">
          <div className="text-6xl mb-4">💧</div>
          <h1 className="text-3xl font-bold text-blue-600 mb-2">Water Buddy</h1>
          <p className="text-gray-600 mb-6">Stay fresh through the day, let Water Buddy guide your way</p>
          <button
            onClick={() => setScreen('name')}
            className="w-full bg-sky-400 hover:bg-sky-500 text-white font-semibold py-3 px-6 rounded-full transition"
          >
            Continue
          </button>
        </div>
      </div>
    );
  }

  // Name Screen
  if (screen === 'name') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-6">
            <User className="w-12 h-12 mx-auto text-blue-600 mb-4" />
            <h2 className="text-2xl font-bold text-gray-800">What is your name?</h2>
            <p className="text-gray-600 text-sm mt-2">Only used to personalize your experience</p>
          </div>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl mb-6 focus:border-blue-400 focus:outline-none"
          />
          <button
            onClick={() => name && setScreen('age')}
            disabled={!name}
            className="w-full bg-sky-400 hover:bg-sky-500 disabled:bg-gray-300 text-white font-semibold py-3 px-6 rounded-full transition"
          >
            Continue
          </button>
        </div>
      </div>
    );
  }

  // Age Group Screen
  if (screen === 'age') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Select your age group</h2>
            <p className="text-gray-600 text-sm">Water intake is based on age-specific health standards</p>
          </div>
          <div className="space-y-3 mb-6">
            {Object.entries(ageGroups).map(([group, data]) => (
              <button
                key={group}
                onClick={() => setAgeGroup(group)}
                className={`w-full p-4 rounded-xl border-2 transition ${
                  ageGroup === group
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-300 hover:border-blue-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="text-left">
                    <div className="font-semibold text-gray-800">{data.emoji} {group}</div>
                    <div className="text-sm text-gray-600">~{data.goal} ml</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
          <button
            onClick={() => ageGroup && setScreen('gender')}
            disabled={!ageGroup}
            className="w-full bg-sky-400 hover:bg-sky-500 disabled:bg-gray-300 text-white font-semibold py-3 px-6 rounded-full transition"
          >
            Continue
          </button>
        </div>
      </div>
    );
  }

  // Gender Screen
  if (screen === 'gender') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Choose your gender</h2>
            <p className="text-gray-600 text-sm">We use your body type to tailor your daily water intake</p>
          </div>
          <div className="grid grid-cols-2 gap-4 mb-6">
            <button
              onClick={() => setGender('Male')}
              className={`p-6 rounded-xl border-2 transition ${
                gender === 'Male'
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-blue-300'
              }`}
            >
              <div className="text-4xl mb-2">👨</div>
              <div className="font-semibold">Male</div>
            </button>
            <button
              onClick={() => setGender('Female')}
              className={`p-6 rounded-xl border-2 transition ${
                gender === 'Female'
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-blue-300'
              }`}
            >
              <div className="text-4xl mb-2">👩</div>
              <div className="font-semibold">Female</div>
            </button>
          </div>
          <button
            onClick={() => gender && setScreen('weight')}
            disabled={!gender}
            className="w-full bg-sky-400 hover:bg-sky-500 disabled:bg-gray-300 text-white font-semibold py-3 px-6 rounded-full transition"
          >
            Continue
          </button>
        </div>
      </div>
    );
  }

  // Weight Screen
  if (screen === 'weight') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">What is your weight?</h2>
            <p className="text-gray-600 text-sm">Your ideal daily water intake is closely tied to your body weight</p>
          </div>
          <div className="flex gap-2 mb-4">
            <button
              onClick={() => setUnit('kg')}
              className={`flex-1 py-2 rounded-lg ${
                unit === 'kg' ? 'bg-blue-500 text-white' : 'bg-gray-200'
              }`}
            >
              kg
            </button>
            <button
              onClick={() => setUnit('lbs')}
              className={`flex-1 py-2 rounded-lg ${
                unit === 'lbs' ? 'bg-blue-500 text-white' : 'bg-gray-200'
              }`}
            >
              lbs
            </button>
          </div>
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl mb-6 text-center text-2xl focus:border-blue-400 focus:outline-none"
          />
          <button
            onClick={() => weight && setScreen('goal')}
            disabled={!weight}
            className="w-full bg-sky-400 hover:bg-sky-500 disabled:bg-gray-300 text-white font-semibold py-3 px-6 rounded-full transition"
          >
            Continue
          </button>
        </div>
      </div>
    );
  }

  // Goal Screen
  if (screen === 'goal') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-6">
            <Target className="w-12 h-12 mx-auto text-blue-600 mb-4" />
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Your Daily Goal</h2>
            <p className="text-gray-600 text-sm">You can tap and setup your own manual daily goal</p>
          </div>
          <div className="text-center mb-6">
            <input
              type="number"
              value={dailyGoal}
              onChange={(e) => setDailyGoal(parseInt(e.target.value) || 0)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl text-center text-4xl font-bold text-blue-600 focus:border-blue-400 focus:outline-none"
            />
            <div className="text-gray-600 mt-2">ml per day</div>
          </div>
          <button
            onClick={() => setScreen('tracker')}
            className="w-full bg-sky-400 hover:bg-sky-500 text-white font-semibold py-3 px-6 rounded-full transition"
          >
            Start Tracking
          </button>
        </div>
      </div>
    );
  }

  // Main Tracker Screen
  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-100 to-blue-200 p-4">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="bg-white rounded-3xl shadow-lg p-6 mb-4">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">{name}</h1>
              <div className="text-gray-600 text-sm">
                {new Date().toLocaleDateString('en-US', { weekday: 'long' })}
              </div>
            </div>
            <button
              onClick={() => setScreen('welcome')}
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              <Settings className="w-6 h-6 text-gray-600" />
            </button>
          </div>

          {/* Progress Stats */}
          <div className="text-center mb-4">
            <div className="text-5xl font-bold text-blue-600 mb-1">
              {totalIntake}ml
            </div>
            <div className="text-gray-600 mb-2">{percentage.toFixed(0)}%</div>
            <div className="text-gray-600 text-sm">
              Remaining: {remaining}ml
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-4 mb-4 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-400 to-cyan-500 h-full transition-all duration-500 rounded-full"
              style={{ width: `${percentage}%` }}
            />
          </div>

          {/* Droppy Message */}
          <div className={`text-center ${message.color} font-semibold`}>
            {message.text}
          </div>
        </div>

        {/* Quick Add Buttons */}
        <div className="bg-white rounded-3xl shadow-lg p-6 mb-4">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Quick Add</h2>
          <div className="grid grid-cols-3 gap-3 mb-4">
            {[250, 500, 750].map((amount) => (
              <button
                key={amount}
                onClick={() => addWater(amount)}
                className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-4 rounded-xl transition"
              >
                +{amount}ml
              </button>
            ))}
          </div>

          {/* Custom Amount */}
          <div className="flex gap-2">
            <input
              type="number"
              value={customAmount}
              onChange={(e) => setCustomAmount(e.target.value)}
              placeholder="Custom ml"
              className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-xl focus:border-blue-400 focus:outline-none"
            />
            <button
              onClick={() => {
                const amount = parseInt(customAmount);
                if (amount > 0) addWater(amount);
              }}
              className="bg-cyan-500 hover:bg-cyan-600 text-white p-3 rounded-xl transition"
            >
              <Plus className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-3xl shadow-lg p-6">
          <button
            onClick={resetIntake}
            className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-6 rounded-xl transition flex items-center justify-center gap-2"
          >
            <RotateCcw className="w-5 h-5" />
            Reset Today's Progress
          </button>
        </div>

        {/* Footer Info */}
        <div className="text-center mt-4 text-gray-600 text-sm">
          <div>Daily Goal: {dailyGoal}ml</div>
          <div>{ageGroup}</div>
        </div>
      </div>
    </div>
  );
};

export default WaterBuddyApp;
