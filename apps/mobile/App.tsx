import React from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'expo-status-bar';
import { View, StyleSheet } from 'react-native';
import HomeScreen from './screens/HomeScreen';
import LoginScreen from './screens/LoginScreen';
import RegisterScreen from './screens/RegisterScreen';
import JobSearchScreen from './screens/JobSearchScreen';
import CareerPathScreen from './screens/CareerPathScreen';
import ProfileScreen from './screens/ProfileScreen';
import LanguageSelector from './components/LanguageSelector';
import { APIProvider } from './context/APIContext';
import { AuthProvider } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <SafeAreaProvider>
      <APIProvider>
        <AuthProvider>
          <LanguageProvider>
            <NavigationContainer>
              <StatusBar style="auto" />
              <Stack.Navigator
                initialRouteName="Home"
                screenOptions={{
                  headerStyle: {
                    backgroundColor: '#4CAF50',
                  },
                  headerTintColor: '#fff',
                  headerTitleStyle: {
                    fontWeight: 'bold',
                  },
                }}
              >
                <Stack.Screen
                  name="Home"
                  component={HomeScreen}
                  options={{ title: 'Green Matchers' }}
                />
                <Stack.Screen
                  name="Login"
                  component={LoginScreen}
                  options={{ title: 'Login' }}
                />
                <Stack.Screen
                  name="Register"
                  component={RegisterScreen}
                  options={{ title: 'Register' }}
                />
                <Stack.Screen
                  name="JobSearch"
                  component={JobSearchScreen}
                  options={{ title: 'Job Search' }}
                />
                <Stack.Screen
                  name="CareerPath"
                  component={CareerPathScreen}
                  options={{ title: 'Career Path' }}
                />
                <Stack.Screen
                  name="Profile"
                  component={ProfileScreen}
                  options={{ title: 'My Profile' }}
                />
              </Stack.Navigator>
              <LanguageSelector />
            </NavigationContainer>
          </LanguageProvider>
        </AuthProvider>
      </APIProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
});