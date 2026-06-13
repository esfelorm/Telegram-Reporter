import os
import asyncio
import json
import random
from datetime import datetime
from typing import Optional, Dict, List
from banner import banner
try:
    from telethon import TelegramClient
    from telethon.tl.types import (User, Channel, Chat,
        InputReportReasonSpam, InputReportReasonPornography,
        InputReportReasonViolence, InputReportReasonChildAbuse,
        InputReportReasonCopyright, InputReportReasonFake,
        InputReportReasonIllegalDrugs, InputReportReasonPersonalDetails
    )
    from telethon.tl.functions import account
    from telethon.errors import FloodWaitError, SessionPasswordNeededError
except ImportError:
    os.system("pip install telethon")
    from telethon import TelegramClient
    from telethon.tl.types import (User, Channel, Chat,
        InputReportReasonSpam, InputReportReasonPornography,
        InputReportReasonViolence, InputReportReasonChildAbuse,
        InputReportReasonCopyright, InputReportReasonFake,
        InputReportReasonIllegalDrugs, InputReportReasonPersonalDetails
    )
    from telethon.tl.functions import account
    from telethon.errors import FloodWaitError, SessionPasswordNeededError


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def clear():
    os.system('cls || clear')

class AccountManager:
    def __init__(self):
        self.accounts_file = "accounts.json"
        self.sessions_dir = "sessions"
        self.accounts = self.load_accounts()
        
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
    
    def load_accounts(self) -> Dict:
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_accounts(self):
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=2)
    
    def get_next_account_number(self) -> int:
        existing = self.list_accounts()
        if not existing:
            return 1
        numbers = []
        for acc in existing:
            if acc.startswith("account_"):
                try:
                    num = int(acc.split('_')[1])
                    numbers.append(num)
                except:
                    pass
        if numbers:
            return max(numbers) + 1
        return 1
    
    def add_account(self, api_id: int, api_hash: str, phone: str, has_2fa: bool = False, password: str = None, first_name: str = "", username: str = ""):
        account_num = self.get_next_account_number()
        name = f"account_{account_num}"
        
        self.accounts[name] = {
            'name': name,
            'number': account_num,
            'api_id': api_id,
            'api_hash': api_hash,
            'phone': phone,
            'has_2fa': has_2fa,
            'password': password,
            'first_name': first_name,
            'username': username,
            'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_file': f"{self.sessions_dir}/{name}.session",
            'total_reports_sent': 0
        }
        self.save_accounts()
        return name
    
    def update_account_stats(self, name: str, reports_sent: int):
        if name in self.accounts:
            self.accounts[name]['total_reports_sent'] = self.accounts[name].get('total_reports_sent', 0) + reports_sent
            self.save_accounts()
    
    def set_2fa(self, name: str, password: str):
        if name in self.accounts:
            self.accounts[name]['has_2fa'] = True
            self.accounts[name]['password'] = password
            self.save_accounts()
            return True
        return False
    
    def get_account(self, name: str) -> Optional[Dict]:
        return self.accounts.get(name)
    
    def list_accounts(self) -> List[str]:
        return list(self.accounts.keys())
    
    def remove_account(self, name: str):
        if name in self.accounts:
            session_file = self.accounts[name]['session_file']
            if os.path.exists(session_file):
                try:
                    os.remove(session_file)
                except:
                    pass
            del self.accounts[name]
            self.save_accounts()
            return True
        return False
    
    def logout_account(self, name: str):
        if name in self.accounts:
            session_file = self.accounts[name]['session_file']
            if os.path.exists(session_file):
                try:
                    os.remove(session_file)
                    return True
                except:
                    return False
        return False


class SmartReporter:
    REPORT_TEMPLATES = {
        '1': {
            'name': 'Spam',
            'reason': 'spam',
            'reason_class': InputReportReasonSpam,
            'messages': [
                "This account is sending massive spam messages repeatedly",
                "Unsolicited promotional content and mass messaging",
                "Automated bot sending spam to multiple users",
                "Repetitive unwanted advertising messages"
            ]
        },
        '2': {
            'name': 'Pornography',
            'reason': 'pornography',
            'reason_class': InputReportReasonPornography,
            'messages': [
                "Sharing explicit adult content without age restriction",
                "Distributing pornographic material publicly",
                "Unsolicited sexual content to users",
                "Posting inappropriate NSFW content"
            ]
        },
        '3': {
            'name': 'Violence',
            'reason': 'violence',
            'reason_class': InputReportReasonViolence,
            'messages': [
                "Promoting violence and physical harm",
                "Encouraging aggressive behavior towards others",
                "Sharing extremely violent content",
                "Threatening users with physical violence"
            ]
        },
        '4': {
            'name': 'Child Abuse',
            'reason': 'child_abuse',
            'reason_class': InputReportReasonChildAbuse,
            'messages': [
                "URGENT: Suspected child exploitation material",
                "CRITICAL: Content involving minors inappropriately",
                "IMMEDIATE REPORT: Possible child safety violation",
                "Violation of child protection policies"
            ]
        },
        '5': {
            'name': 'Copyright',
            'reason': 'copyright',
            'reason_class': InputReportReasonCopyright,
            'messages': [
                "Unauthorized distribution of copyrighted material",
                "Sharing pirated content without permission",
                "Copyright infringement of original works",
                "Distributing content without proper licensing"
            ]
        },
        '6': {
            'name': 'Fake Account',
            'reason': 'fake',
            'reason_class': InputReportReasonFake,
            'messages': [
                "Impersonating a real person or brand",
                "Fraudulent account pretending to be someone else",
                "Fake identity and profile information",
                "Deceptive account for scamming purposes"
            ]
        },
        '7': {
            'name': 'Illegal Drugs',
            'reason': 'illegal_drugs',
            'reason_class': InputReportReasonIllegalDrugs,
            'messages': [
                "Promoting and selling illegal substances",
                "Distribution of controlled substances",
                "Advertising drug paraphernalia",
                "Offering illegal narcotics for sale"
            ]
        },
        '8': {
            'name': 'Personal Details',
            'reason': 'personal_details',
            'reason_class': InputReportReasonPersonalDetails,
            'messages': [
                "Sharing private information without consent",
                "Exposing personal details of individuals",
                "Doxxing and privacy violation",
                "Violation of privacy policies"
            ]
        }
    }
    
    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager
        self.clients = {}
    
    def print_colored(self, text: str, color: str = 'WHITE', end: str = '\n'):
        color_code = getattr(Colors, color.upper(), Colors.WHITE)
        print(f"{color_code}{text}{Colors.RESET}", end=end)
    
    def get_input(self, prompt: str, color: str = 'CYAN') -> str:
        self.print_colored(prompt, color, end='')
        return input()
    
    async def get_client(self, account_name: str):
        account_info = self.account_manager.get_account(account_name)
        if not account_info:
            return None
        
        if account_name in self.clients:
            client = self.clients[account_name]
            if client.is_connected():
                return client
        
        session_file = account_info['session_file']
        
        client = TelegramClient(
            session_file,
            account_info['api_id'],
            account_info['api_hash']
        )
        
        await client.connect()
        
        if not await client.is_user_authorized():
            self.print_colored(f"\nSession expired or not found for {account_name}", 'YELLOW')
            self.print_colored(f"Please login again to create session...", 'CYAN')
            
            await client.send_code_request(account_info['phone'])
            code = self.get_input(f"Enter code for {account_info['phone']}: ", 'YELLOW')
            
            try:
                await client.sign_in(account_info['phone'], code)
            except SessionPasswordNeededError:
                if account_info['has_2fa'] and account_info['password']:
                    password = account_info['password']
                else:
                    password = self.get_input("Enter 2FA password: ", 'YELLOW')
                    if not account_info['has_2fa']:
                        self.account_manager.set_2fa(account_name, password)
                await client.sign_in(password=password)
            
            self.print_colored(f"✓ Session created for {account_name}", 'GREEN')
        
        self.clients[account_name] = client
        return client
    
    async def detect_target_type(self, client, target_input: str):
        target_input = target_input.strip()
        target_input = target_input.replace('https://t.me/', '').replace('@', '')
        
        try:
            entity = await client.get_entity(target_input)
            
            if isinstance(entity, User):
                return 'user', entity
            elif isinstance(entity, Channel):
                if hasattr(entity, 'megagroup') and entity.megagroup:
                    return 'group', entity
                else:
                    return 'channel', entity
            elif isinstance(entity, Chat):
                return 'group', entity
            else:
                return 'unknown', None
        except Exception as e:
            return 'unknown', None
    
    async def report_target(self, client, account_info, target_entity, target_type, reason_class, message: str, count: int):
        account_display_name = account_info.get('first_name', account_info['name'])
        success = 0
        
        try:
            peer = await client.get_input_entity(target_entity.id)
        except Exception as e:
            self.print_colored(f"  ✗ [{account_display_name}] Cannot get peer: {str(e)}", 'RED')
            return 0
        
        for i in range(count):
            try:
                await client(
                    account.ReportPeerRequest(
                        peer=peer,
                        reason=reason_class(),
                        message=message
                    )
                )
                success += 1
                self.print_colored(f"  ✓ [{account_display_name}] Report {i+1}/{count} sent", 'GREEN')
                
                if i < count - 1:
                    await asyncio.sleep(random.uniform(1, 2))
                    
            except FloodWaitError as e:
                self.print_colored(f"  ⏳ [{account_display_name}] Rate limited! Waiting {e.seconds}s", 'YELLOW')
                await asyncio.sleep(e.seconds)
            except Exception as e:
                self.print_colored(f"  ✗ [{account_display_name}] Error: {str(e)[:80]}", 'RED')
                await asyncio.sleep(1)
        
        return success
    
    async def add_account(self):
        self.print_colored("\n=== Add New Account ===", 'CYAN')
        
        api_id = int(self.get_input("API ID: ", 'YELLOW'))
        api_hash = self.get_input("API Hash: ", 'YELLOW')
        phone = self.get_input("Phone number (with +): ", 'YELLOW')
        
        self.print_colored(f"\nLogging in to {phone}...", 'CYAN')
        
        account_num = self.account_manager.get_next_account_number()
        name = f"account_{account_num}"
        session_file = f"sessions/{name}.session"
        
        client = TelegramClient(session_file, api_id, api_hash)
        
        try:
            await client.connect()
            
            await client.send_code_request(phone)
            code = self.get_input("Enter verification code: ", 'YELLOW')
            
            try:
                await client.sign_in(phone, code)
                has_2fa = False
                password = None
            except SessionPasswordNeededError:
                self.print_colored("2FA detected!", 'YELLOW')
                password = self.get_input("Enter 2FA password: ", 'YELLOW')
                await client.sign_in(password=password)
                has_2fa = True
            
            me = await client.get_me()
            first_name = me.first_name or ""
            username = f"@{me.username}" if me.username else "No username"
            
            self.print_colored(f"\n✓ Successfully logged in as: {first_name}", 'GREEN')
            self.print_colored(f"✓ Session saved to: {session_file}", 'GREEN')
            
            self.account_manager.add_account(api_id, api_hash, phone, has_2fa, password, first_name, username)
            
            await client.disconnect()
            
            self.print_colored(f"\n✓ Account '{first_name}' added successfully!", 'GREEN')
            return True
            
        except Exception as e:
            self.print_colored(f"\nLogin failed: {str(e)}", 'RED')
            await client.disconnect()
            if os.path.exists(session_file):
                try:
                    os.remove(session_file)
                except:
                    pass
            return False
    
    async def reporting_flow(self):
        accounts = self.account_manager.list_accounts()
        
        if not accounts:
            self.print_colored("No accounts found! Please add an account first.", 'RED')
            return
        clear()
        print (Colors.RED,banner.banner())
        self.print_colored("\n" + "="*70, 'CYAN')
        self.print_colored("SELECT ACCOUNT", 'CYAN')
        self.print_colored("="*70, 'CYAN')
        
        account_list = []
        self.print_colored(f"\n{'#':<4} {'Account Name':<30} {'Status':<12} {'Reports':<10}", 'YELLOW')
        self.print_colored("-"*70, 'CYAN')
        
        for idx, acc_name in enumerate(accounts, 1):
            acc_info = self.account_manager.get_account(acc_name)
            session_exists = os.path.exists(acc_info['session_file'])
            status = "✓ Active" if session_exists else "✗ No Session"
            status_color = Colors.GREEN if session_exists else Colors.RED
            reports = acc_info.get('total_reports_sent', 0)
            self.print_colored(f"{idx:<4} {acc_info['first_name']:<30} {status_color}{status:<12}{Colors.RESET} {reports:<10}", 'WHITE')
            account_list.append((acc_name, acc_info))
        
        self.print_colored("="*70, 'CYAN')
        
        while True:
            try:
                acc_choice = self.get_input("\nSelect account number: ", 'YELLOW')
                selected_idx = int(acc_choice) - 1
                if 0 <= selected_idx < len(account_list):
                    selected_account_name, selected_account_info = account_list[selected_idx]
                    break
                else:
                    self.print_colored(f"Invalid! Please enter 1-{len(account_list)}", 'RED')
            except ValueError:
                self.print_colored("Invalid! Please enter a number.", 'RED')
        
        self.print_colored(f"\n✓ Selected: {selected_account_info['first_name']}", 'GREEN')
        
        self.print_colored("\n" + "="*70, 'CYAN')
        self.print_colored("CONNECTING ACCOUNT", 'CYAN')
        self.print_colored("="*70, 'CYAN')
        
        client = await self.get_client(selected_account_name)
        if not client:
            self.print_colored("Failed to connect account!", 'RED')
            return
        
        try:
            me = await client.get_me()
            self.print_colored(f"✓ Connected as: {me.first_name}", 'GREEN')
        except:
            self.print_colored("✗ Connection failed!", 'RED')
            await client.disconnect()
            return
        
        target = self.get_input("\nTarget username or channel link: ", 'YELLOW')
        
        target_type, target_entity = await self.detect_target_type(client, target)
        
        if target_type == 'user':
            self.print_colored(f"\n✓ Target: USER ACCOUNT", 'GREEN')
        elif target_type == 'channel':
            self.print_colored(f"\n✓ Target: CHANNEL", 'GREEN')
        elif target_type == 'group':
            self.print_colored(f"\n✓ Target: GROUP", 'GREEN')
        else:
            self.print_colored("Target not found!", 'RED')
            await client.disconnect()
            return
        
        self.print_colored("\n=== Report Reasons ===", 'CYAN')
        for key, data in self.REPORT_TEMPLATES.items():
            self.print_colored(f"{key}. {data['name']}", 'WHITE')
        
        reason_choice = self.get_input("\nReason (1-8): ", 'YELLOW')
        
        if reason_choice not in self.REPORT_TEMPLATES:
            self.print_colored("Invalid!", 'RED')
            await client.disconnect()
            return
        
        reason_data = self.REPORT_TEMPLATES[reason_choice]
        
        self.print_colored(f"\n=== Messages for {reason_data['name']} ===", 'CYAN')
        for idx, msg in enumerate(reason_data['messages'], 1):
            self.print_colored(f"{idx}. {msg}", 'WHITE')
        
        msg_choice = self.get_input("\nChoose (1-4) or 'custom': ", 'YELLOW')
        
        if msg_choice.lower() == 'custom':
            report_message = self.get_input("Custom message: ", 'YELLOW')
        elif msg_choice.isdigit() and 1 <= int(msg_choice) <= len(reason_data['messages']):
            report_message = reason_data['messages'][int(msg_choice) - 1]
        else:
            report_message = reason_data['messages'][0]
        
        report_count = int(self.get_input("Number of reports to send: ", 'YELLOW'))
        
        if report_count > 20:
            confirm = self.get_input(f"{report_count} reports is high! Continue? (y/n): ", 'RED')
            if confirm.lower() != 'y':
                await client.disconnect()
                return
        
        self.print_colored(f"\n{'='*60}", 'CYAN')
        self.print_colored(f"REPORTING DETAILS", 'CYAN')
        self.print_colored(f"Account: {selected_account_info['first_name']}", 'YELLOW')
        self.print_colored(f"Target: {target} ({target_type})", 'YELLOW')
        self.print_colored(f"Reason: {reason_data['name']}", 'YELLOW')
        self.print_colored(f"Reports to send: {report_count}", 'YELLOW')
        self.print_colored(f"{'='*60}", 'CYAN')
        
        confirm_start = self.get_input("\nStart sending reports? (y/n): ", 'RED')
        if confirm_start.lower() != 'y':
            self.print_colored("Cancelled by user.", 'YELLOW')
            await client.disconnect()
            return
        
        print()
        self.print_colored(f"\n>>> {selected_account_info['first_name']} reporting...", 'PURPLE')
        
        result = await self.report_target(client, selected_account_info, target_entity, target_type, reason_data['reason_class'], report_message, report_count)
        
        self.account_manager.update_account_stats(selected_account_name, result)
        
        if result == report_count:
            self.print_colored(f"\n✅ {selected_account_info['first_name']}: {result}/{report_count} reports sent successfully", 'GREEN')
        else:
            self.print_colored(f"\n⚠️ {selected_account_info['first_name']}: {result}/{report_count} reports sent", 'YELLOW')
        
        await client.disconnect()
        
        total_all = 0
        for acc in self.account_manager.list_accounts():
            acc_info = self.account_manager.get_account(acc)
            total_all += acc_info.get('total_reports_sent', 0)
        
        print()
        self.print_colored(f"{'='*60}", 'CYAN')
        self.print_colored(f"ALL TIME TOTAL: {total_all} reports", 'PURPLE')
        self.print_colored(f"{'='*60}", 'CYAN')
    
    async def manage_accounts(self):
        while True:
            clear()
            print (Colors.CYAN,banner.banner())
            self.print_colored("\n=== Account Management ===", 'CYAN')
            self.print_colored("="*50, 'CYAN')
            self.print_colored("1. Add new account", 'GREEN')
            self.print_colored("2. List all accounts", 'GREEN')
            self.print_colored("3. Remove account (delete from system)", 'GREEN')
            self.print_colored("4. Logout account (delete session only)", 'GREEN')
            self.print_colored("5. Back to main menu", 'GREEN')
            self.print_colored("="*50, 'CYAN')
            
            choice = self.get_input("\nOption: ", 'YELLOW')
            
            if choice == '1':
                await self.add_account()
                self.get_input("\nPress Enter...", 'CYAN')
                
            elif choice == '2':
                accounts = self.account_manager.list_accounts()
                if accounts:
                    self.print_colored("\n" + "="*90, 'CYAN')
                    self.print_colored(f"{'#':<4} {'First Name':<25} {'Phone':<15} {'2FA':<8} {'Session':<12} {'Reports':<8}", 'YELLOW')
                    self.print_colored("="*90, 'CYAN')
                    for idx, acc in enumerate(accounts, 1):
                        info = self.account_manager.get_account(acc)
                        status = "Yes" if info['has_2fa'] else "No"
                        session_exists = os.path.exists(info['session_file'])
                        session_text = "✓ Exists" if session_exists else "✗ Missing"
                        session_color = Colors.GREEN if session_exists else Colors.RED
                        reports = info.get('total_reports_sent', 0)
                        self.print_colored(f"{idx:<4} {info['first_name']:<25} {info['phone']:<15} {status:<8} {session_color}{session_text:<12}{Colors.RESET} {reports:<8}", 'WHITE')
                    self.print_colored("="*90, 'CYAN')
                else:
                    self.print_colored("No accounts!", 'YELLOW')
                
                self.get_input("\nPress Enter...", 'CYAN')
                
            elif choice == '3':
                accounts = self.account_manager.list_accounts()
                if not accounts:
                    self.print_colored("No accounts!", 'YELLOW')
                    await asyncio.sleep(1)
                    continue
                
                self.print_colored("\n=== Remove Account ===", 'CYAN')
                self.print_colored("-"*50, 'CYAN')
                for idx, acc in enumerate(accounts, 1):
                    info = self.account_manager.get_account(acc)
                    self.print_colored(f"{idx}. {info['first_name']} - {info['phone']}", 'WHITE')
                self.print_colored("-"*50, 'CYAN')
                
                try:
                    acc_choice = self.get_input("\nAccount number: ", 'YELLOW')
                    selected_idx = int(acc_choice) - 1
                    if 0 <= selected_idx < len(accounts):
                        to_remove = accounts[selected_idx]
                        removed_name = self.account_manager.get_account(to_remove)['first_name']
                        confirm = self.get_input(f"Remove '{removed_name}'? (y/n): ", 'RED')
                        if confirm.lower() == 'y':
                            self.account_manager.remove_account(to_remove)
                            self.print_colored(f"✓ {removed_name} removed", 'GREEN')
                    else:
                        self.print_colored("Invalid!", 'RED')
                except:
                    self.print_colored("Invalid!", 'RED')
                
                await asyncio.sleep(1)
                
            elif choice == '4':
                accounts = self.account_manager.list_accounts()
                if not accounts:
                    self.print_colored("No accounts!", 'YELLOW')
                    await asyncio.sleep(1)
                    continue
                
                self.print_colored("\n=== Logout Account ===", 'CYAN')
                self.print_colored("-"*50, 'CYAN')
                for idx, acc in enumerate(accounts, 1):
                    info = self.account_manager.get_account(acc)
                    session_icon = "✓" if os.path.exists(info['session_file']) else "✗"
                    self.print_colored(f"{idx}. {info['first_name']} - {info['phone']} [{session_icon}]", 'WHITE')
                self.print_colored("-"*50, 'CYAN')
                
                try:
                    acc_choice = self.get_input("\nAccount number: ", 'YELLOW')
                    selected_idx = int(acc_choice) - 1
                    if 0 <= selected_idx < len(accounts):
                        to_logout = accounts[selected_idx]
                        logout_name = self.account_manager.get_account(to_logout)['first_name']
                        confirm = self.get_input(f"Logout '{logout_name}'? (y/n): ", 'RED')
                        if confirm.lower() == 'y':
                            if self.account_manager.logout_account(to_logout):
                                self.print_colored(f"✓ {logout_name} logged out", 'GREEN')
                            else:
                                self.print_colored(f"✗ No session found", 'YELLOW')
                    else:
                        self.print_colored("Invalid!", 'RED')
                except:
                    self.print_colored("Invalid!", 'RED')
                
                await asyncio.sleep(1)
                
            elif choice == '5':
                break
    
    async def run(self):
        while True:
            clear()
            
            print (f"""
{Colors.CYAN}{Colors.BOLD}
{banner.banner()}
{Colors.RESET}
""")
            
            total_reports = 0
            accounts_list = self.account_manager.list_accounts()
            active_sessions = 0
            for acc in accounts_list:
                info = self.account_manager.get_account(acc)
                total_reports += info.get('total_reports_sent', 0)
                if os.path.exists(info['session_file']):
                    active_sessions += 1
            
            self.print_colored(f"Accounts: {len(accounts_list)} | Active Sessions: {active_sessions} | Total Reports: {total_reports}", 'PURPLE')
            print()
            
            self.print_colored("1. Start Reporting", 'GREEN')
            self.print_colored("2. Manage Accounts", 'GREEN')
            self.print_colored("3. Reporter VIP (Upgrade)", 'YELLOW')
            self.print_colored("3. Exit", 'GREEN')
            
            choice = self.get_input("\nOption: ", 'YELLOW')
            
            if choice == '1':
                await self.reporting_flow()
                self.get_input("\nPress Enter...", 'CYAN')
            elif choice == '2':
                await self.manage_accounts()
            elif choice == '3':
                clear()
                print (banner.get_vip_info())
                exit()
            elif choice == '4':
                self.print_colored("\nGoodbye!", 'GREEN')
                break
            else:
                self.print_colored("Invalid!", 'RED')
                await asyncio.sleep(1)


async def main():
    account_manager = AccountManager()
    reporter = SmartReporter(account_manager)
    await reporter.run()

if __name__ == "__main__":
    asyncio.run(main())
