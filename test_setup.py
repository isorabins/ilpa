# test_setup.py - Run this BEFORE starting development
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_cli_tool(tool_name, command):
    """Check if a CLI tool is installed and accessible"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {tool_name} is installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"❌ {tool_name} is not installed or not accessible")
        print(f"   Fix: Install {tool_name} and ensure it's in your PATH")
        return False

def check_environment_variable(var_name, required=True):
    """Check if an environment variable is set"""
    value = os.getenv(var_name)
    if value:
        # Show first few chars for security
        masked_value = value[:8] + "..." if len(value) > 8 else value
        print(f"✅ {var_name} is set: {masked_value}")
        return True
    else:
        if required:
            print(f"❌ {var_name} is not set")
            print(f"   Fix: Add {var_name} to your .env file")
        else:
            print(f"⚠️  {var_name} is not set (optional)")
        return not required

def check_project_structure():
    """Check if the project structure is properly set up"""
    print("\n🏗️  Checking project structure...\n")
    
    required_dirs = [
        'backend',
        'frontend',
        '.taskmaster',
        '.taskmaster/docs',
        '.taskmaster/tasks'
    ]
    
    required_files = [
        '.env',
        '.gitignore',
        '.taskmaster/docs/prd.txt'
    ]
    
    f4_reference_dirs = [
        'fridays-at-four',
        'FAF_website'
    ]
    
    all_good = True
    
    # Check required directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
    
    # Check required files
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    # Check F@4 reference directories
    for dir_path in f4_reference_dirs:
        if Path(dir_path).exists():
            print(f"✅ F@4 reference directory exists: {dir_path}")
        else:
            print(f"⚠️  F@4 reference directory missing: {dir_path}")
            print(f"   Fix: Clone {dir_path} for reference")
    
    return all_good

def test_api_connections():
    """Test API connections with actual requests"""
    print("\n🧪 Testing API connections...\n")
    
    all_good = True
    
    # Test Anthropic API
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": "Say 'API working'"}],
            max_tokens=10
        )
        print("✅ Anthropic API working")
    except ImportError:
        print("❌ Anthropic library not installed")
        print("   Fix: pip install anthropic")
        all_good = False
    except Exception as e:
        print(f"❌ Anthropic API failed: {e}")
        print("   Fix: Check ANTHROPIC_API_KEY in .env")
        all_good = False
    
    # Test OpenAI API
    try:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Say 'API working'"}],
            max_tokens=10
        )
        print("✅ OpenAI API working")
    except ImportError:
        print("❌ OpenAI library not installed")
        print("   Fix: pip install openai")
        all_good = False
    except Exception as e:
        print(f"❌ OpenAI API failed: {e}")
        print("   Fix: Check OPENAI_API_KEY in .env")
        all_good = False
    
    # Test Supabase connection
    try:
        from supabase import create_client
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_ANON_KEY")
        )
        # Simple query to test connection - will fail gracefully if no tables exist yet
        try:
            result = supabase.table('conversations').select("*").limit(1).execute()
            print("✅ Supabase connection working (conversations table exists)")
        except:
            # Try a simple auth check instead
            result = supabase.auth.get_session()
            print("✅ Supabase connection working (basic connection established)")
    except ImportError:
        print("❌ Supabase library not installed")
        print("   Fix: pip install supabase")
        all_good = False
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("   Fix: Check SUPABASE_URL and SUPABASE_ANON_KEY in .env")
        all_good = False
    
    return all_good

def main():
    """Main function to run all setup verification checks"""
    print("🎯 ILPA Pre-Flight Setup Verification")
    print("=" * 50)
    
    # Check CLI tools
    print("\n🔧 Checking CLI tools...\n")
    cli_checks = [
        check_cli_tool("Python", "python"),
        check_cli_tool("Node.js", "node"),
        check_cli_tool("Git", "git"),
        check_cli_tool("Heroku CLI", "heroku"),
        check_cli_tool("Vercel CLI", "vercel")
    ]
    
    # Check environment variables
    print("\n🔐 Checking environment variables...\n")
    env_checks = [
        check_environment_variable("ANTHROPIC_API_KEY"),
        check_environment_variable("OPENAI_API_KEY"),
        check_environment_variable("SUPABASE_URL"),
        check_environment_variable("SUPABASE_ANON_KEY"),
        check_environment_variable("JWT_SECRET_KEY", required=False),
        check_environment_variable("SUPABASE_SERVICE_KEY", required=False)
    ]
    
    # Check project structure
    structure_check = check_project_structure()
    
    # Test API connections
    api_check = test_api_connections()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    all_cli_good = all(cli_checks)
    all_env_good = all(env_checks)
    
    print(f"CLI Tools: {'✅ PASS' if all_cli_good else '❌ FAIL'}")
    print(f"Environment Variables: {'✅ PASS' if all_env_good else '❌ FAIL'}")
    print(f"Project Structure: {'✅ PASS' if structure_check else '❌ FAIL'}")
    print(f"API Connections: {'✅ PASS' if api_check else '❌ FAIL'}")
    
    if all_cli_good and all_env_good and structure_check and api_check:
        print("\n🎉 ALL CHECKS PASSED! Ready for Day 1 development!")
        return 0
    else:
        print("\n🚨 SOME CHECKS FAILED! Fix the issues above before starting development.")
        print("\nFor help, check the Pre-Flight Checklist in .taskmaster/docs/prd.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 