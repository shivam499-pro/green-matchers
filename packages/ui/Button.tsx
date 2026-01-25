import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
// For web: import { TouchableOpacity, Text, StyleSheet } from 'react-native-web';

interface ButtonProps {
  title: string;
  onPress: () => void;
  style?: ViewStyle;
  textStyle?: TextStyle;
  disabled?: boolean;
  type?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  style,
  textStyle,
  disabled = false,
  type = 'primary',
  size = 'medium',
}) => {
  // Get styles based on type and size
  const getButtonStyle = (): ViewStyle => {
    const baseStyle = styles.button;
    let typeStyle = {};
    let sizeStyle = {};

    // Type styles
    if (type === 'primary') {
      typeStyle = styles.primaryButton;
    } else if (type === 'secondary') {
      typeStyle = styles.secondaryButton;
    } else if (type === 'danger') {
      typeStyle = styles.dangerButton;
    }

    // Size styles
    if (size === 'small') {
      sizeStyle = styles.smallButton;
    } else if (size === 'large') {
      sizeStyle = styles.largeButton;
    }

    return { ...baseStyle, ...typeStyle, ...sizeStyle, ...style };
  };

  const getTextStyle = (): TextStyle => {
    const baseStyle = styles.buttonText;
    let typeStyle = {};

    if (type === 'secondary') {
      typeStyle = styles.secondaryButtonText;
    } else if (type === 'danger') {
      typeStyle = styles.dangerButtonText;
    }

    return { ...baseStyle, ...typeStyle, ...textStyle };
  };

  return (
    <TouchableOpacity
      style={getButtonStyle()}
      onPress={onPress}
      disabled={disabled}
      activeOpacity={0.8}
    >
      <Text style={getTextStyle()}>{title}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  primaryButton: {
    backgroundColor: '#4CAF50',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#4CAF50',
  },
  dangerButton: {
    backgroundColor: '#F44336',
  },
  buttonText: {
    fontSize: 16,
    fontWeight: '600',
    color: 'white',
    textAlign: 'center',
  },
  secondaryButtonText: {
    color: '#4CAF50',
  },
  dangerButtonText: {
    color: 'white',
  },
  smallButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  largeButton: {
    paddingVertical: 16,
    paddingHorizontal: 32,
  },
});

// Export for both web and mobile
export default Button;