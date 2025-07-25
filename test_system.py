#!/usr/bin/env python3
"""
Arthur Passuello CV System Testing Script
Validates that the markdown-based system preserves the LaTeX conditional logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_system import CVBuilder
import yaml
from pathlib import Path


class CVSystemTester:
    def __init__(self):
        self.builder = CVBuilder()
        self.test_results = []
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append({
            'name': test_name,
            'passed': passed,
            'message': message
        })
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
    
    def test_version_configurations(self):
        """Test that all version configurations are properly defined"""
        print("\n=== Testing Version Configurations ===")
        
        expected_versions = ['firmware', 'ai', 'consulting', 'executive', 'general']
        
        for version in expected_versions:
            config = self.builder.versions.get(version)
            self.log_test(
                f"Version {version} exists",
                config is not None,
                f"Config: {config}" if config else "Missing configuration"
            )
            
            if config:
                # Test required fields
                required_fields = ['toggles', 'tagline', 'max_priority', 'layout']
                for field in required_fields:
                    self.log_test(
                        f"Version {version} has {field}",
                        field in config,
                        f"Value: {config.get(field)}" if field in config else "Missing field"
                    )
    
    def test_skills_processing(self):
        """Test skills section processing logic"""
        print("\n=== Testing Skills Processing ===")
        
        # Mock skills data
        mock_skills = {
            'executive': {
                'leadership_impact': [
                    {'skill': 'Technical Team Leadership', 'metric': '7+ Direct Reports', 'type': 'leadmetric'}
                ]
            },
            'technical': {
                'programming_languages': {
                    'firmware': ['C/C++ (Expert)', 'Python (Expert)'],
                    'ai': ['Python (Expert)', 'C/C++'],
                    'consulting': ['Python (Expert)', 'JavaScript']
                }
            }
        }
        
        # Test executive layout
        exec_result = self.builder.process_skills_section(mock_skills, 'executive')
        self.log_test(
            "Executive skills layout",
            exec_result.get('layout') == 'executive',
            f"Layout: {exec_result.get('layout')}"
        )
        
        # Test technical layout for different versions
        for version in ['firmware', 'ai', 'consulting']:
            tech_result = self.builder.process_skills_section(mock_skills, version)
            self.log_test(
                f"Technical skills layout for {version}",
                tech_result.get('layout') == 'technical',
                f"Layout: {tech_result.get('layout')}"
            )
            
            # Test version-specific programming languages
            expected_langs = mock_skills['technical']['programming_languages'][version]
            actual_langs = tech_result.get('programming_languages', [])
            self.log_test(
                f"Programming languages for {version}",
                actual_langs == expected_langs,
                f"Expected: {expected_langs}, Actual: {actual_langs}"
            )
    
    def test_experience_processing(self):
        """Test experience section processing logic"""
        print("\n=== Testing Experience Processing ===")
        
        # Mock experience data
        mock_experience = {
            'experiences': [
                {
                    'company': 'Test Company',
                    'location': 'Test Location',
                    'period': '2020 - Present',
                    'reference': '',
                    'versions': ['firmware', 'ai'],
                    'position_base': 'Engineer',
                    'position_variants': {
                        'firmware': 'Firmware Engineer',
                        'ai': 'AI Engineer'
                    },
                    'skills_tags': {
                        'firmware': 'C++, Embedded, RTOS',
                        'ai': 'Python, ML, PyTorch'
                    },
                    'achievements': [
                        {
                            'text': 'Achievement 1',
                            'versions': ['firmware'],
                            'priority': 1
                        },
                        {
                            'text': 'Achievement 2',
                            'versions': ['firmware', 'ai'],
                            'priority': 2
                        },
                        {
                            'text': 'Achievement 3',
                            'versions': ['all'],
                            'priority': 3
                        }
                    ]
                }
            ]
        }
        
        # Test firmware version (max_priority = 3)
        firmware_result = self.builder.process_experience_section(mock_experience, 'firmware')
        self.log_test(
            "Firmware experience inclusion",
            len(firmware_result) == 1,
            f"Found {len(firmware_result)} experiences"
        )
        
        if firmware_result:
            exp = firmware_result[0]
            self.log_test(
                "Firmware position title",
                exp['position'] == 'Firmware Engineer',
                f"Position: {exp['position']}"
            )
            
            # Should have 3 achievements (priority 1, 2, 3)
            self.log_test(
                "Firmware achievements count",
                len(exp['achievements']) == 3,
                f"Found {len(exp['achievements'])} achievements"
            )
        
        # Test executive version (max_priority = 1)
        exec_result = self.builder.process_experience_section(mock_experience, 'executive')
        self.log_test(
            "Executive experience exclusion",
            len(exec_result) == 0,
            f"Found {len(exec_result)} experiences (should be 0 since not in versions)"
        )
        
        # Test AI version
        ai_result = self.builder.process_experience_section(mock_experience, 'ai')
        if ai_result:
            exp = ai_result[0]
            # Should have 2 achievements (priority 1 is firmware-only, priority 2 is both, priority 3 is all)
            expected_achievements = 2  # priority 2 and 3 only
            self.log_test(
                "AI achievements filtering",
                len(exp['achievements']) == expected_achievements,
                f"Expected {expected_achievements}, got {len(exp['achievements'])}"
            )
    
    def test_projects_processing(self):
        """Test projects section processing logic"""
        print("\n=== Testing Projects Processing ===")
        
        # Mock projects data
        mock_projects = {
            'projects': [
                {
                    'name': 'Test Project',
                    'period': '2023',
                    'links': {
                        'github': 'https://github.com/test/project'
                    },
                    'versions': ['firmware', 'ai'],
                    'descriptions': {
                        'firmware': ['Firmware description'],
                        'ai': ['AI description']
                    },
                    'skills_tags': {
                        'firmware': 'C++, RTOS, Hardware',
                        'ai': 'Python, PyTorch, ML'
                    }
                }
            ]
        }
        
        # Test firmware version
        firmware_result = self.builder.process_projects_section(mock_projects, 'firmware')
        self.log_test(
            "Firmware project inclusion",
            len(firmware_result) == 1,
            f"Found {len(firmware_result)} projects"
        )
        
        if firmware_result:
            project = firmware_result[0]
            self.log_test(
                "Firmware project description",
                project['descriptions'] == ['Firmware description'],
                f"Description: {project['descriptions']}"
            )
        
        # Test executive version (should have no projects)
        exec_result = self.builder.process_projects_section(mock_projects, 'executive')
        self.log_test(
            "Executive projects exclusion",
            len(exec_result) == 0,
            f"Found {len(exec_result)} projects (should be 0 for executive)"
        )
        
        # Test consulting version (not in project versions)
        consulting_result = self.builder.process_projects_section(mock_projects, 'consulting')
        self.log_test(
            "Consulting project exclusion",
            len(consulting_result) == 0,
            f"Found {len(consulting_result)} projects (should be 0 - not in versions)"
        )
    
    def test_priority_filtering(self):
        """Test priority-based filtering logic"""
        print("\n=== Testing Priority Filtering ===")
        
        test_items = [
            {'priority': 1, 'text': 'Priority 1'},
            {'priority': 2, 'text': 'Priority 2'},
            {'priority': 3, 'text': 'Priority 3'},
            {'text': 'No priority (default 1)'}  # Should default to priority 1
        ]
        
        # Test executive version (max_priority = 1)
        exec_filtered = self.builder.filter_by_priority(test_items, 'executive')
        self.log_test(
            "Executive priority filtering",
            len(exec_filtered) == 2,  # Priority 1 and default
            f"Expected 2 items, got {len(exec_filtered)}"
        )
        
        # Test firmware version (max_priority = 3)
        firmware_filtered = self.builder.filter_by_priority(test_items, 'firmware')
        self.log_test(
            "Firmware priority filtering",
            len(firmware_filtered) == 4,  # All items
            f"Expected 4 items, got {len(firmware_filtered)}"
        )
        
        # Test general version (max_priority = 2)
        general_filtered = self.builder.filter_by_priority(test_items, 'general')
        self.log_test(
            "General priority filtering",
            len(general_filtered) == 3,  # Priority 1, 2, and default
            f"Expected 3 items, got {len(general_filtered)}"
        )
    
    def test_version_conditions(self):
        """Test version condition checking"""
        print("\n=== Testing Version Conditions ===")
        
        # Test "all" versions
        self.log_test(
            "All versions condition",
            self.builder.check_version_condition(['all'], 'firmware'),
            "Should return True for 'all' versions"
        )
        
        # Test specific version
        self.log_test(
            "Specific version condition - match",
            self.builder.check_version_condition(['firmware', 'ai'], 'firmware'),
            "Should return True when version matches"
        )
        
        self.log_test(
            "Specific version condition - no match",
            not self.builder.check_version_condition(['ai', 'consulting'], 'firmware'),
            "Should return False when version doesn't match"
        )
        
        # Test empty versions list
        self.log_test(
            "Empty versions condition",
            self.builder.check_version_condition([], 'firmware'),
            "Should return True for empty versions list"
        )
    
    def test_markdown_generation(self):
        """Test markdown generation for different sections"""
        print("\n=== Testing Markdown Generation ===")
        
        # Test skills markdown generation
        mock_skills = {
            'technical': {
                'programming_languages': {
                    'firmware': ['C/C++', 'Python']
                },
                'core_technologies': {
                    'firmware': ['FreeRTOS', 'STM32']
                }
            }
        }
        
        skills_md = self.builder.generate_skills_markdown(mock_skills, 'firmware')
        self.log_test(
            "Skills markdown generation",
            '## Skills' in skills_md and 'C/C++' in skills_md,
            "Generated markdown should contain section header and skills"
        )
        
        # Test experience markdown generation
        mock_experience = {
            'experiences': [
                {
                    'company': 'Test Company',
                    'location': 'Test Location',
                    'period': 'Test Period',
                    'position': 'Test Position',
                    'reference': '',
                    'achievements': [
                        {'text': 'Test achievement', 'type': 'base', 'priority': 1}
                    ]
                }
            ]
        }
        
        exp_md = self.builder.generate_experience_markdown(mock_experience, 'firmware')
        self.log_test(
            "Experience markdown generation",
            '## Work Experience' in exp_md and 'Test Company' in exp_md,
            "Generated markdown should contain section header and company"
        )
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Running Arthur Passuello CV System Tests")
        print("=" * 50)
        
        self.test_version_configurations()
        self.test_skills_processing()
        self.test_experience_processing()
        self.test_projects_processing()
        self.test_priority_filtering()
        self.test_version_conditions()
        self.test_markdown_generation()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! System is ready for use.")
        else:
            print("❌ Some tests failed. Check the output above for details.")
            
            # Show failed tests
            failed_tests = [result for result in self.test_results if not result['passed']]
            if failed_tests:
                print("\nFailed tests:")
                for test in failed_tests:
                    print(f"  - {test['name']}: {test['message']}")
        
        return passed_tests == total_tests


def main():
    """Main test function"""
    tester = CVSystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 System is ready for building CV versions!")
        print("Next steps:")
        print("1. Run: python scripts/build-cv.py --test")
        print("2. Run: python scripts/build-cv.py all")
        print("3. Check output files in output/ directory")
    else:
        print("\n🔧 Fix the issues above before proceeding.")
        sys.exit(1)


if __name__ == '__main__':
    main()