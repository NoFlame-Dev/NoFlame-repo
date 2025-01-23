import React from 'react';
import { SafeAreaView, TouchableOpacity, Text } from 'react-native';

export default function Box() {
  return (
    <SafeAreaView
      style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}
    >
      {/* All corners */}
      <TouchableOpacity style={{ backgroundColor: '#147EFB', padding: 10, borderRadius: 4 }}>
        <Text style={{ color: '#fff' }}>Click me!</Text>
      </TouchableOpacity>

      {/* Individual corners */}
      <TouchableOpacity
        style={{
          backgroundColor: '#147EFB',
          padding: 10,
          borderTopLeftRadius: 6,
          borderBottomRightRadius: 6,
        }}
      >
        <Text style={{ color: '#fff' }}>Click me!</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}