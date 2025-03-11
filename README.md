# OneDrive via Rclone
OneDrive via Rclone is een Windows programma waarmee je OneDrive bestanden kan bekijken en bewerken via de Windows verkenner. Het voordeel van OneDrive via Rclone is dat gedeelde mappen lokaal bekeken en bewerkt kunnen worden.

## OneDrive via Rclone installeren
1. Download de bestanden (rechtsboven groene knop **<> Code** en dan **Download ZIP**)
2. Unzip de bestanden naar een locatie naar keuze.
3. Ga naar de folder **OneDrive-via-Rclone-main**. Dubbelklik het bestand **InstallRclone.exe** om Rclone te installeren. Indien Windows zegt dat het een onbekende app is, klik dan op **Meer informatie** en dan op **Toch uitvoeren**.
4. Dubbelklik het bestand **ConfigureOneDrive.exe** om OneDrive te verbinden met Rclone. Er zal nu twee keer worden gevraagd om in te loggen met OneDrive, en om de locatie waar OneDrive via Rclone moet worden geinstalleerd.
5. Als de installatie voltooid is, moet uw computer herstart worden om OneDrive via Rclone te starten. Er zal nu op de locatie die in de vorige stap is gekozen is een map genaamd **OneDriveRclone** worden gemaakt. Hier kunt u uw OneDrive bestanden vinden.

## OneDrive via Rclone verwijderen
1. Dubbelklik **Uninstall.exe** om OneDrive via Rclone van uw computer te verwijderen. Uw bestanden in OneDrive worden niet verwijderd.

## Verdere info
- OneDrive via Rclone zal automatisch worden opgestart bij het starten van de computer. Er opent kort een command window, sluit deze niet.
- OneDrive via Rclone kan ook handmatig worden gestart door het bestand **MountOneDrive.bat** te dubbelklikken in de folder **Scripts**.
- Verwijder de folder **Scripts** niet, deze is nodig om OneDrive via Rclone op te starten.
- Om van OneDrive account te switchen, dubbelklik eerst op **Uninstall.exe** om het huidige account te verwijderen. Dubbelklik daarna **ConfigureOneDrive.exe** om met het andere account in te loggen.
