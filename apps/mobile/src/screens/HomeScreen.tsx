import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { API_ENDPOINTS, handleApiError } from '../config/api';
import axios from 'axios';
import { MaterialIcons } from '@expo/vector-icons';

const HomeScreen = () => {
  const navigation = useNavigation();
  const { language } = useLanguage();
  const { user, token } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await axios.get(API_ENDPOINTS.STATS, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          timeout: 10000,
        });

        setStats(response.data);
      } catch (error) {
        const handledError = handleApiError(error);
        setError(handledError.error);
        console.error('Failed to fetch stats:', handledError.error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [token]);

  const renderFeatureCard = (title: string, description: string, icon: string, onPress: () => void) => (
    <TouchableOpacity style={styles.featureCard} onPress={onPress}>
      <MaterialIcons name={icon as any} size={32} color="#4CAF50" />
      <Text style={styles.featureTitle}>{title}</Text>
      <Text style={styles.featureDescription}>{description}</Text>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Loading Green Matchers...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <MaterialIcons name="error" size={48} color="#F44336" />
        <Text style={styles.errorText}>{error}</Text>
        <TouchableOpacity
          style={styles.retryButton}
          onPress={() => {
            setLoading(true);
            setError(null);
            // Retry logic would go here
          }}
        >
          <Text style={styles.retryButtonText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>🌱 Green Matchers</Text>
        <Text style={styles.subtitle}>
          {language === 'hi' ? 'सतत करियर के लिए AI-पावर्ड प्लेटफॉर्म' :
           language === 'bn' ? 'টেকসই ক্যারিয়ারের জন্য AI-পাওয়ার্ড প্ল্যাটফর্ম' :
           'AI-Powered Platform for Sustainable Careers'}
        </Text>

        {user ? (
          <View style={styles.userInfo}>
            <Text style={styles.welcomeText}>Welcome back, {user.username}!</Text>
            <Text style={styles.userRole}>Role: {user.role}</Text>
          </View>
        ) : (
          <View style={styles.authButtons}>
            <TouchableOpacity
              style={styles.authButton}
              onPress={() => navigation.navigate('Login' as never)}
            >
              <Text style={styles.authButtonText}>Login</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.authButton, styles.registerButton]}
              onPress={() => navigation.navigate('Register' as never)}
            >
              <Text style={styles.authButtonText}>Register</Text>
            </TouchableOpacity>
          </View>
        )}
      </View>

      {stats && (
        <View style={styles.statsContainer}>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{stats.total_jobs || '50+'}</Text>
            <Text style={styles.statLabel}>Green Jobs</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{stats.companies || '50+'}</Text>
            <Text style={styles.statLabel}>Companies</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{stats.sdg_goals || '15'}</Text>
            <Text style={styles.statLabel}>SDG Goals</Text>
          </View>
        </View>
      )}

      <View style={styles.featuresSection}>
        <Text style={styles.sectionTitle}>🤖 AI-Powered Features</Text>

        <View style={styles.featuresGrid}>
          {renderFeatureCard(
            language === 'hi' ? 'करियर मिलान' : language === 'bn' ? 'ক্যারিয়ার মিলান' : 'Career Matching',
            language === 'hi' ? 'आपके कौशल से सही करियर मिलाएं' : language === 'bn' ? 'আপনার দক্ষতার সাথে সঠিক ক্যারিয়ার মিলান' : 'Match your skills to perfect careers',
            'work',
            () => navigation.navigate('CareerPath' as never)
          )}

          {renderFeatureCard(
            language === 'hi' ? 'नौकरी खोज' : language === 'bn' ? 'চাকরি অনুসন্ধান' : 'Job Search',
            language === 'hi' ? 'AI के साथ हरे नौकरियां खोजें' : language === 'bn' ? 'AI দিয়ে সবুজ চাকরি খুঁজুন' : 'Find green jobs with AI',
            'search',
            () => navigation.navigate('JobSearch' as never)
          )}

          {renderFeatureCard(
            language === 'hi' ? 'भाषा अनुवाद' : language === 'bn' ? 'ভাষা অনুবাদ' : 'Language Translation',
            language === 'hi' ? '10 भारतीय भाषाओं में अनुवाद' : language === 'bn' ? '10 ভারতীয় ভাষায় অনুবাদ' : 'Translate in 10 Indian languages',
            'translate',
            () => navigation.navigate('LanguageDemo' as never)
          )}

          {renderFeatureCard(
            language === 'hi' ? 'प्रोफाइल प्रबंधन' : language === 'bn' ? 'প্রোফাইল ব্যবস্থাপনা' : 'Profile Management',
            language === 'hi' ? 'अपना प्रोफाइल और रिज्यूमे प्रबंधित करें' : language === 'bn' ? 'আপনার প্রোফাইল এবং রেজিউমে পরিচালনা করুন' : 'Manage your profile and resume',
            'person',
            () => navigation.navigate('Profile' as never)
          )}
        </View>
      </View>

      <View style={styles.aboutSection}>
        <Text style={styles.sectionTitle}>🌍 About Green Matchers</Text>
        <Text style={styles.aboutText}>
          {language === 'hi' ? (
            'ग्रीन मैचर्स एक AI-पावर्ड प्लेटफॉर्म है जो नौकरी तलाशने वालों को टिकाऊ करियर के साथ जोड़ता है। हम मारियाDB वेक्टर खोज और बहुभाषी NLP का उपयोग करते हैं ताकि 10 भारतीय भाषाओं में व्यक्तिगत करियर सिफारिशें प्रदान की जा सकें।'
          ) : language === 'bn' ? (
            'গ্রিন ম্যাচার্স হল একটি AI-পাওয়ার্ড প্ল্যাটফর্ম যা চাকরি প্রার্থীদের টেকসই ক্যারিয়ারের সাথে সংযুক্ত করে। আমরা MariaDB ভেক্টর অনুসন্ধান এবং মাল্টিলিংগুয়াল NLP ব্যবহার করি 10 ভারতীয় ভাষায় ব্যক্তিগতকৃত ক্যারিয়ার সুপারিশ প্রদান করতে।'
          ) : (
            'Green Matchers is an AI-powered platform that connects job seekers with sustainable careers. We use MariaDB vector search and multilingual NLP to provide personalized career recommendations in 10 Indian languages.'
          )}
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#4CAF50',
    padding: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    marginBottom: 15,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    marginBottom: 15,
  },
  userInfo: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    padding: 10,
    borderRadius: 8,
    marginTop: 10,
  },
  welcomeText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  userRole: {
    color: 'white',
    fontSize: 14,
  },
  authButtons: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 15,
  },
  authButton: {
    backgroundColor: 'white',
    padding: 10,
    borderRadius: 8,
    flex: 1,
  },
  authButtonText: {
    color: '#4CAF50',
    textAlign: 'center',
    fontWeight: 'bold',
  },
  registerButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: 'white',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 15,
    backgroundColor: 'white',
    margin: 15,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  statCard: {
    alignItems: 'center',
    padding: 10,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  featuresSection: {
    padding: 15,
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  featuresGrid: {
    gap: 15,
  },
  featureCard: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
    marginBottom: 15,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 10,
    marginBottom: 5,
  },
  featureDescription: {
    fontSize: 14,
    color: '#666',
  },
  aboutSection: {
    padding: 15,
    backgroundColor: 'white',
    margin: 15,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  aboutText: {
    fontSize: 14,
    color: '#555',
    lineHeight: 22,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 15,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  errorText: {
    marginTop: 15,
    fontSize: 16,
    color: '#F44336',
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: '#4CAF50',
    padding: 12,
    borderRadius: 8,
    width: 120,
  },
  retryButtonText: {
    color: 'white',
    textAlign: 'center',
    fontWeight: 'bold',
  },
});

export default HomeScreen;